import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import os
import tempfile
import tarfile
import unittest
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.refs=[]; self.ids=set(); self.scripts=[]; self.h1=0; self.alternate=False; self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.add(a['id'])
        if tag == 'h1': self.h1 += 1
        if tag == 'script': self.scripts.append(a)
        if tag == 'link' and a.get('type') == 'text/markdown': self.alternate=True
        for name in ['href','src','action','formaction']:
            if name in a: self.refs.append(a[name])

# This is a strict evaluator of the keywords used in our schema, avoiding a runtime dependency.
def validate(value, spec, schema, path='$'):
    if '$ref' in spec:
        node=schema
        for key in spec['$ref'][2:].split('/'): node=node[key]
        validate(value,node,schema,path); return
    if 'const' in spec: assert value==spec['const'], path
    if 'enum' in spec: assert value in spec['enum'], path
    kinds=spec.get('type',[]); kinds=[kinds] if isinstance(kinds,str) else kinds
    matches={'object':isinstance(value,dict),'array':isinstance(value,list),'string':isinstance(value,str),'boolean':isinstance(value,bool),'integer':type(value) is int,'number':type(value) in (int,float),'null':value is None}
    if kinds: assert any(matches[k] for k in kinds), path
    if isinstance(value,dict):
        assert all(k in value for k in spec.get('required',[])), path+' required'
        props=spec.get('properties',{})
        for key,item in value.items():
            if key in props: validate(item,props[key],schema,path+'.'+key)
            elif spec.get('additionalProperties') is False: raise AssertionError(path+' unexpected '+key)
            elif isinstance(spec.get('additionalProperties'),dict): validate(item,spec['additionalProperties'],schema,path+'.'+key)
    if isinstance(value,list):
        assert len(value)>=spec.get('minItems',0),path
        assert len(value)<=spec.get('maxItems',len(value)),path
        for i,item in enumerate(value): validate(item,spec.get('items',{}),schema,path+str(i))
    if isinstance(value,str):
        assert len(value)>=spec.get('minLength',0),path
        if 'pattern' in spec: assert re.search(spec['pattern'],value),path
    if type(value) in (int,float): assert value>=spec.get('minimum',value),path

class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run(['python3','scripts/build.py'],cwd=ROOT,check=True)
        cls.data=json.loads((DIST/'mine.json').read_text())

    def resolve(self, ref, source):
        parts=urlsplit(ref)
        if parts.scheme or parts.netloc: return
        path=unquote(parts.path)
        if path.startswith('/'): base=DIST/path.lstrip('/')
        elif path: base=source.parent/path
        else: base=source
        candidates=[base,base.with_suffix('.html'),base/'index.html'] if path else [source]
        if path=='/': candidates=[DIST/'index.html']
        existing=next((p for p in candidates if p.is_file()),None)
        self.assertIsNotNone(existing, f'{source}: {ref}')
        if parts.fragment and existing.suffix=='.html': self.assertIn(parts.fragment,Page(existing.read_text()).ids,f'{source}: {ref}')

    def test_links_and_twins(self):
        for source in DIST.rglob('*.html'):
            page=Page(source.read_text())
            self.assertEqual(page.h1,1,source)
            self.assertTrue(page.alternate,source)
            self.assertTrue(source.with_suffix('.md').exists(),source)
            for ref in page.refs: self.resolve(ref,source)
            self.assertTrue(all('src' in script for script in page.scripts),source)
        for source in [DIST/'llms.txt',*DIST.rglob('*.md')]:
            for ref in re.findall(r'\]\(([^)]+)\)',source.read_text()): self.resolve(ref,source)

    def test_manifest_schema_and_source_authority(self):
        schema=json.loads((ROOT/'schemas/mine.schema.json').read_text()); validate(self.data,schema,schema)
        release=json.loads((DIST/'releases/current.json').read_text())
        for key in ['status','requirements','pools']: self.assertEqual(self.data[key],release[key])
        self.assertIs(type(self.data['status']['live']), bool)
        self.assertEqual(self.data['status']['launch_status'], 'live' if self.data['status']['live'] else 'registered_starting_soon')
        self.assertEqual(self.data['status']['netuid'], 92)
        self.assertFalse(self.data['source']['public'])
        self.assertFalse(release['images']['public'])
        self.assertEqual([t['id'] for t in self.data['agent_tiers']],['A','B','C'])
        self.assertEqual(self.data['integrity']['sha256'],hashlib.sha256((DIST/'kit'/self.data['integrity']['tarball']).read_bytes()).hexdigest())
        with tarfile.open(DIST/'kit'/self.data['integrity']['tarball']) as archive:
            pinned = json.loads(archive.extractfile('releases/current.json').read())
            # Site onboarding status is intentionally newer than the kit archive.
            # All immutable release data must still match; only status is overlaid.
            site_release = json.loads(json.dumps(release))
            pinned['status'] = site_release['status']
            self.assertEqual(pinned, site_release)
            self.assertEqual(release['status']['notes'], self.data['copy']['CHECKER_BODY'])
            version_source = archive.extractfile('reaxlib/__init__.py').read().decode()
            kit_version = re.search(r'__version__\s*=\s*[\"\']([^\"\']+)', version_source).group(1)
            self.assertEqual(self.data['integrity']['version'],kit_version)
            self.assertEqual(self.data['integrity']['tarball'],'reax-miner-kit-'+kit_version+'.tar.gz')
            self.assertEqual(self.data['integrity']['release_id'],release['release_id'])
        for step in self.data['mainnet_steps']:
            self.assertEqual(step['blocked_until_live'],step['id'] not in ['doctor','choose-mode'])
            if step['cost']['kind']=='tao': self.assertEqual(step['who'],'human')
        self.assertIs(type(self.data['status']['live']), bool)

    def test_release_packaging_refuses_missing_or_invalid_semver(self):
        before=(ROOT/'kit.lock.json').read_bytes()
        for source in ['"""No version yet."""', '__version__ = "1.1.0rc2"']:
            with self.subTest(source=source), tempfile.TemporaryDirectory(prefix='dm-version-check-') as scratch:
                repo=Path(scratch)
                (repo/'reaxlib').mkdir(); (repo/'releases').mkdir()
                (repo/'reaxlib/__init__.py').write_text(source)
                (repo/'releases/current.json').write_text((ROOT/'site/releases/current.json').read_text())
                def git(*args):
                    subprocess.run(['git','-C',str(repo),*args],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                git('init'); git('add','.')
                git('-c','user.name=Site test','-c','user.email=site-test@example.invalid','commit','-m','Fixture')
                result=subprocess.run(['python3',str(ROOT/'scripts/release-kit.py'),str(repo)],capture_output=True,text=True)
                self.assertNotEqual(result.returncode,0)
                self.assertIn('version',result.stderr)
                self.assertEqual((ROOT/'kit.lock.json').read_bytes(),before)

    def test_recorded_doctor_samples_match_pinned_archive(self):
        provenance=json.loads((ROOT/'content/samples/provenance.json').read_text())
        self.assertEqual(provenance['kit_commit'], self.data['integrity']['commit'])
        self.assertEqual(provenance['archive_sha256'], self.data['integrity']['sha256'])
        with tarfile.open(DIST/'kit'/self.data['integrity']['tarball']) as archive:
            for ident,receipt in provenance['samples'].items():
                self.assertEqual(hashlib.sha256(archive.extractfile(receipt['fixture']).read()).hexdigest(),receipt['fixture_sha256'])
                output=(ROOT/('content/samples/doctor-'+ident+'.txt')).read_bytes()
                self.assertEqual(hashlib.sha256(output).hexdigest(),receipt['output_sha256'])
        self.assertIn('Host checked. The free rehearsal needs the REAX source, which is private until launch.', (ROOT/'content/samples/doctor-no-gpu.txt').read_text())
        self.assertNotIn('warning:', (ROOT/'content/samples/doctor-4090.txt').read_text())
        self.assertNotIn('80 GB', (ROOT/'content/samples/doctor-4090.txt').read_text())
        self.assertNotIn('our build host',(DIST/'index.html').read_text())

    def test_schema_rejects_bad_inputs(self):
        schema=json.loads((ROOT/'schemas/mine.schema.json').read_text())
        bad=json.loads(json.dumps(self.data)); bad['steps'][0]['who']='bot'
        with self.assertRaises(AssertionError): validate(bad,schema,schema)
        bad=json.loads(json.dumps(self.data)); bad['integrity']['sha256']='fake'
        with self.assertRaises(AssertionError): validate(bad,schema,schema)

    def test_wording_and_placeholders(self):
        forbidden=['earn per day','guaranteed','helsinki','finland','to the moon','passive income']
        for source in [*DIST.rglob('*.html'),*DIST.rglob('*.md'),DIST/'mine.json',DIST/'llms-full.txt']:
            text=source.read_text().lower()
            for word in forbidden + ['unverified', 'rehearse free today', 'free rehearsal is available']: self.assertNotIn(word,text,str(source))
            # Required risk disclaimer and lead-authored negation are the only exceptions.
            text=text.replace('not investment advice','').replace('never call this an investment','')
            self.assertNotRegex(text,r'\binvest\w*',str(source))
            self.assertNotRegex(text,r'\{\{[a-z_]+\}\}',str(source))

    def test_launch_state_copy_and_steps(self):
        import runpy
        import shutil
        module = runpy.run_path(str(ROOT/'scripts/build.py'))
        build = module['build']
        globals_ = build.__globals__
        with tempfile.TemporaryDirectory(prefix='dm-launch-states-') as scratch:
            root = Path(scratch)
            for name in ['site', 'content', 'templates', 'schemas']:
                shutil.copytree(ROOT/name, root/name)
            for name in ['kit.lock.json', 'nginx.conf']:
                shutil.copy2(ROOT/name, root/name)
            globals_['ROOT'] = root
            globals_['DIST'] = root/'dist'
            release_path = root/'site/releases/current.json'
            release = json.loads(release_path.read_text())
            cases = [
                ('pending', False, False, False),
                ('live-private', True, False, False),
                ('live-public', True, True, True),
                ('source-public-pending', False, True, False),
            ]
            for name, live, source_public, images_public in cases:
                with self.subTest(state=name):
                    candidate = json.loads(json.dumps(release))
                    candidate['status']['live'] = live
                    candidate['status']['launch_status'] = 'live' if live else 'registered_starting_soon'
                    candidate['source']['public'] = source_public
                    candidate['images']['public'] = images_public
                    candidate['status']['netuid'] = 92
                    candidate['status']['testnet_netuid'] = None
                    release_path.write_text(json.dumps(candidate))
                    build()
                    output = root/'dist'
                    data = json.loads((output/'mine.json').read_text())
                    validate(data, json.loads((ROOT/'schemas/mine.schema.json').read_text()), json.loads((ROOT/'schemas/mine.schema.json').read_text()))
                    home = (output/'index.html').read_text()
                    pages = '\n'.join(p.read_text() for p in [*output.rglob('*.html'), *output.rglob('*.md'), output/'llms.txt'])
                    self.assertNotIn('UNVERIFIED', pages)
                    self.assertNotIn('Rehearse free today', pages)
                    if name == 'pending':
                        self.assertEqual(data['state'], 'prelaunch')
                        self.assertIn('Registered as netuid 92, starting soon.', home)
                        self.assertIn('Alpha trading and emission remain disabled until the subnet owner starts it.', home)
                        self.assertIn('Source and images stay private until launch', (output/'llms.txt').read_text())
                        self.assertIn('authorized localnet rehearsal needs REAX_SOURCE_DIR', (output/'llms.txt').read_text())
                        self.assertTrue(all(s['command'] and s['blocked_until_live'] for s in data['steps'][2:]))
                        self.assertIn('stop before install', data['steps'][1]['verify'].lower())
                        self.assertTrue(all(s['blocked_until_live'] for s in data['mainnet_steps'][2:]))
                    elif name == 'live-private':
                        self.assertEqual(data['state'], 'live')
                        self.assertIn('Network live', home)
                        self.assertIn('source remains private', home.lower())
                        self.assertIn('alpha trading and epochs have started', home.lower())
                        self.assertIn('separate root-gated subnet emission flag', home.lower())
                        self.assertIn('can be zero', home.lower())
                        self.assertIn('live chain alone does not satisfy the source gate', (output/'agent.md').read_text().lower())
                        self.assertTrue(all(s['blocked_until_live'] for s in data['steps'][2:]))
                        self.assertTrue(all(s['blocked_until_live'] for s in data['mainnet_steps'][2:]))
                        self.assertNotEqual(data['prompts']['short'], 'Set up this machine for mining at Decision Models by REAX: https://mine.decisionmodels.io')
                    elif name == 'live-public':
                        self.assertEqual(data['state'], 'live')
                        self.assertIn('Network live', home)
                        self.assertNotIn('source remains private', home.lower())
                        self.assertTrue(all(not s['blocked_until_live'] for s in data['steps'][2:]))
                        register = next(s for s in data['mainnet_steps'] if s['id']=='register')
                        self.assertFalse(register['blocked_until_live'])
                        self.assertEqual((register['who'], register['cost']['kind']), ('human', 'tao'))
                        self.assertEqual(data['prompts']['short'], 'Set up this machine for mining at Decision Models by REAX: https://mine.decisionmodels.io')
                    else:
                        self.assertEqual(data['state'], 'prelaunch')
                        self.assertIn('starting soon as netuid 92', home)
                        self.assertIn('Practice run available', home)
                        self.assertTrue(all(not s['blocked_until_live'] for s in data['steps'][2:]))
                        self.assertTrue(all(s['blocked_until_live'] for s in data['mainnet_steps'][2:]))
                        self.assertIn('Mainnet registration remains blocked until status.live is true', (output/'llms.txt').read_text())
                    self.assertIn('configured status.testnet_netuid', ' '.join(data['rules']))
                    self.assertIn('Never infer or reuse the Finney mainnet netuid for testnet', ' '.join(data['rules']))
                    self.assertIsNone(data['status']['testnet_netuid'])

    def test_agent_commands_match_manifest(self):
        import shlex
        agent = (DIST/'agent.md').read_text()
        mainnet = agent.split('## Step 4')[1].split('## Step 5')[0]
        commands = [shlex.split(c) for c in re.findall(r'`(\./reaxctl [^`]+)`', mainnet)]
        for step in self.data['mainnet_steps']:
            if step['command'] and step['id'] not in ('doctor', 'choose-mode'):
                # Argument order is immaterial; exact values and approval flags are not.
                expected = shlex.split(step['command'])
                self.assertTrue(any(sorted(c) == sorted(expected) for c in commands), step['id'])
        install = next(s for s in self.data['mainnet_steps'] if s['id'] == 'install')
        self.assertIn('--confirm-mainnet', install['command'])
        self.assertIn('only after the human explicitly approves', mainnet)
        self.assertIn('Python 3.8+', agent)
        self.assertIn('Python 3.10+', agent)
        for step in self.data['steps'][2:]:
            self.assertTrue(step['blocked_until_live'])
            self.assertIn('Authorized localnet rehearsal may use REAX_SOURCE_DIR', step['verify'])

    def test_human_layout_and_copy(self):
        for source in DIST.rglob('*.html'):
            text = source.read_text()
            self.assertEqual(text.count('<table>'), text.count('aria-label="Table"'), source)
            self.assertNotIn('rel="preload"', text)
            if source.name != 'agent.html':
                self.assertNotIn('installation is refused with exit 12', text)
                self.assertNotIn('Before launch, run doctor and plan', text)
        error = (DIST/'404.html').read_text()
        self.assertNotIn('ON THIS PAGE', error)
        self.assertNotIn('Read as Markdown', error)
        home = (DIST/'index.html').read_text()
        if self.data['status']['live']:
            self.assertIn('Network live', home)
            self.assertIn('source remains private', home.lower())
        else:
            self.assertIn('Netuid 92 registered · starting soon', home)
        self.assertRegex(home, r'<div[^>]*aria-label="Prompt variants"[^>]*role="tablist"')
        self.assertRegex(home, r'<form[^>]*class="checker"[^>]*hidden')

    def test_headers_and_installer(self):
        config=(DIST/'nginx.conf').read_text()
        self.assertIn("default-src 'self'",config); self.assertNotIn('unsafe-inline',config)
        self.assertIn('X-Robots-Tag "noindex, nofollow" always',config)
        self.assertIn('Vary Accept always',config)
        installer=DIST/'install.sh'; subprocess.run(['sh','-n',str(installer)],check=True)
        self.assertLessEqual(len(installer.read_text().splitlines()),60)
        self.assertNotIn('sudo', '\n'.join(line for line in installer.read_text().splitlines() if not line.startswith('#')))
        self.assertEqual((DIST/'robots.txt').read_text(),'User-agent: *\nAllow: /\n')

    def test_installer_checksum_and_existing_destination(self):
        # Intercept downloads with a local fake curl; never contact any host.
        with tempfile.TemporaryDirectory(prefix='dm-installer-') as scratch:
            folder=Path(scratch); commands=folder/'bin';commands.mkdir()
            curl=commands/'curl'
            curl.write_text('#!/bin/sh\nwhile [ "$#" -gt 0 ]; do\n if [ "$1" = --output ]; then shift; output=$1; fi\n shift\ndone\ncp "$DM_TEST_PAYLOAD" "$output"\n')
            curl.chmod(0o755)
            target=folder/'kit'; payload=folder/'payload';payload.write_text('wrong archive')
            env=dict(os.environ,PATH=str(commands)+':'+os.environ['PATH'],REAX_KIT_DIR=str(target),DM_TEST_PAYLOAD=str(payload))
            failed=subprocess.run(['sh',str(DIST/'install.sh')],env=env,capture_output=True,text=True)
            self.assertNotEqual(failed.returncode,0);self.assertIn('Checksum mismatch',failed.stderr);self.assertFalse(target.exists())
            env['DM_TEST_PAYLOAD']=str(DIST/'kit'/self.data['integrity']['tarball'])
            passed=subprocess.run(['sh',str(DIST/'install.sh')],env=env,capture_output=True,text=True)
            self.assertEqual(passed.returncode,0,passed.stderr);self.assertTrue((target/'reaxctl').is_file());self.assertIn('Verified kit',passed.stdout)
            blocked=subprocess.run(['sh',str(DIST/'install.sh')],env=env,capture_output=True,text=True)
            self.assertNotEqual(blocked.returncode,0);self.assertIn('already exists',blocked.stderr)
            print('Installer: mismatch refuses extraction; pinned archive succeeds; existing destination preserved')

    def test_landing_transfer_budget(self):
        landing=Page((DIST/'index.html').read_text())
        files={DIST/'index.html',DIST/'mine.json'}
        for ref in landing.refs:
            if ref.startswith('/assets/') and '/fonts/' not in ref: files.add(DIST/ref.lstrip('/'))
            if ref=='/webmcp.js': files.add(DIST/'webmcp.js')
        size=sum(p.stat().st_size for p in files)
        self.assertLess(size,150*1024,f'Landing weight {size} bytes excluding fonts')
        print(f'Landing transfer budget: {size} bytes excluding fonts')

if __name__=='__main__': unittest.main()

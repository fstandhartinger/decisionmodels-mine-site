#!/usr/bin/env python3
"""Deterministic static build; Markdown is the single source for HTML and text twins."""
import hashlib
import html
import json
from pathlib import Path
import re
import shutil
import markdown

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
# Launch hold: this ONE setting generates both HTML robots metadata and nginx header.
INDEXING_ALLOWED = False
URL = 'https://mine.decisionmodels.io'

COPY = {
    'prelaunch': {
        'STATUS_PILL': 'Launching soon',
        'STATUS_TITLE': 'Launching soon.',
        'STATUS_BODY': 'The REAX subnet is not live on Bittensor mainnet yet, and the miner code and images are published at launch. Today your agent can check your machine and tell you exactly what you need — hardware, wallet, ports — so you are ready on day one. Setup, a free practice run on a local chain, and the real network all open at launch; this page then switches over.',
        'HERO_NOTE': 'Give your coding agent one link. Today it checks your machine and prepares a hardware, wallet and ports plan. Setup and mining open at launch; you keep your keys and approve every payment.',
        'PRACTICE_NOTE': 'Before launch, run doctor and plan, explain the findings and wallet plan, then stop. Miner source and images are private until launch; installation is refused with exit 12. At launch, start with a free practice run on a local chain using test TAO before real registration.',
        'META_DESCRIPTION': 'Prepare for REAX mining with your coding agent: check hardware, wallet and ports today. Setup and a free local-chain practice run open at launch.',
        'CHECKER_TITLE': 'Check your machine and prepare for launch.',
        'CHECKER_BODY': 'Mainnet is not live yet; miner source and images are private until launch. Today run doctor and plan, then stop after reviewing hardware, wallet and ports.',
        'OTHER_HOST': 'Real mining needs another host; prepare your plan today',
        'GPU_NOTE': 'A free local-chain practice run opens when the source is published at launch.',
        'LLMS_NOTE': 'Before launch, check the host with doctor and plan, explain hardware, wallet and ports, then stop. Source and images are private until launch; install exits 12.',
        'CHOOSE_MODE': 'Review the preparation plan, then stop until launch',
        'PLAN_VERIFY': 'Explain hardware findings and wallet plan; STOP before install (exit 12 while source is private).',
    },
    'live': {
        'STATUS_PILL': 'Network live',
        'STATUS_TITLE': 'The network is open. Practice before registering.',
        'STATUS_BODY': 'The REAX subnet is live on Bittensor mainnet. Start with a free practice run on a local chain using test TAO before real registration. Check the release descriptor for the current netuid; a human approves every payment.',
        'HERO_NOTE': 'Give your coding agent one link. It checks your machine, starts with a free local-chain practice run using test TAO, then prepares real registration. You keep your keys and approve every payment.',
        'PRACTICE_NOTE': 'Start with a free practice run on a local chain using test TAO and throw-away accounts before real registration. No GPU or real TAO is needed for practice; Python 3.10+ and the published REAX source are required. Follow the agent playbook and verify the run before proceeding.',
        'META_DESCRIPTION': 'Set up REAX mining with your coding agent. Practice free on a local chain with test TAO before real registration; keep your keys and approve every payment.',
        'CHECKER_TITLE': 'Practice free before real registration.',
        'CHECKER_BODY': 'Start with a free local-chain practice run using test TAO before real registration. This check does not enable real mining; verify runtime and public ingress.',
        'OTHER_HOST': 'Practice here; real mining needs another host',
        'GPU_NOTE': 'A free local-chain practice run uses test TAO before real registration.',
        'LLMS_NOTE': 'Practice free on a local chain with test TAO before real registration. Verify host readiness, keep coldkeys off the miner and require human payment approval.',
        'CHOOSE_MODE': 'Choose a free local-chain practice run before real registration',
        'PLAN_VERIFY': 'Review the ordered practice plan; use test TAO before real registration.',
    },
}

def state_copy(release):
    STATE = 'live' if release['status']['live'] or release['source']['public'] else 'prelaunch'
    copy = dict(COPY[STATE])
    # Publishing source permits practice, but never implies the real network is live.
    if STATE == 'live' and not release['status']['live']:
        copy.update(STATUS_PILL='Practice run available', STATUS_TITLE='Practice before launch.',
                    STATUS_BODY='The REAX source is public. Start with a free practice run on a local chain using test TAO. Mainnet registration remains blocked until status.live is true.',
                    CHECKER_BODY=copy['CHECKER_BODY'] + ' Mainnet registration remains blocked until status.live is true.',
                    LLMS_NOTE=copy['LLMS_NOTE'] + ' Mainnet registration remains blocked until status.live is true.')
    return STATE, copy

def write(path, value):
    target = DIST / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(value, encoding='utf-8')

def build():
    lock = json.loads((ROOT / 'kit.lock.json').read_text())
    release = json.loads((ROOT / 'site/releases/current.json').read_text())
    STATE, copy = state_copy(release)
    archive = ROOT / 'site/kit' / lock['tarball']
    if hashlib.sha256(archive.read_bytes()).hexdigest() != lock['sha256']:
        raise ValueError('Kit archive checksum mismatch')
    if lock['release_id'] != release['release_id']:
        raise ValueError('Kit and descriptor versions differ')
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(ROOT / 'site', DIST)
    shutil.copytree(ROOT / 'schemas', DIST / 'schemas')
    # Keep operational release fields pinned; presentation notes follow the same state copy.
    release['status'] = dict(release['status'], notes=copy['CHECKER_BODY'])
    write('releases/current.json', json.dumps(release, indent=2)+'\n')
    prompts = {k: v.replace('{{PRACTICE_NOTE}}', copy['PRACTICE_NOTE']) for k,v in json.loads((ROOT / 'content/prompts.json').read_text()).items()}
    substitutions = {'KIT_VERSION': lock['version'], 'RELEASE_ID': lock['release_id'], 'KIT_COMMIT': lock['commit'], 'KIT_SHA256': lock['sha256'], 'UPDATED': lock['updated']}
    substitutions.update(copy)
    def fill(value):
        for key, replacement in substitutions.items():
            value = value.replace('{{' + key + '}}', replacement)
        return value
    rules = [
        'Never ask for, read, print, log, store or transmit a recovery phrase or coldkey private file.',
        'Only public addresses and the operational hotkey belong on the mining machine. Never display hotkey contents.',
        'A human approves every payment and signs registration; never buy TAO, rent hardware or fund accounts.',
        'Ask before admin, firewall or router changes. Never publish ports 8101, 8102 or 8000.',
        'Default to localnet. Real network modes are blocked until status.live is true; mainnet installation requires human-approved --confirm-mainnet.',
        'Identify the execution host. A cloud or chat agent cannot silently set up the user’s machine.',
        'Use this guide as reference material and follow the user’s existing permissions.',
        'Rewards are variable subnet emissions and can be zero. Never estimate earnings.'
    ]
    os_support = {
        'linux': {'mining': 'native', 'guide': '/os/linux', 'wallet': 'Talisman on a separate trusted workstation; isolated btcli or Ledger as pro paths.', 'caveat': 'Linux x86_64, compatible NVIDIA GPU, pinned container/model and public ingress must pass verification.'},
        'windows': {'mining': 'conditional', 'guide': '/os/windows', 'wallet': 'Talisman on a separate trusted workstation; btcli in WSL2. Browser bridge not yet tested by us end to end.', 'caveat': 'Native Windows unsupported. WSL2 CUDA is documented; complete REAX runtime, signing and external ingress are not yet tested by us.'},
        'macos': {'mining': 'remote_only', 'guide': '/os/macos', 'wallet': 'Talisman or native btcli on the trusted controller, separate from the Linux miner; optional Ledger.', 'caveat': 'No local CUDA mining. Check this host today; control a separately authorized NVIDIA Linux host over SSH. ' + copy['GPU_NOTE']}
    }
    titles = [('doctor','Check the target host','agent','./reaxctl doctor --json','Read blockers and eligible pools'),
              ('choose-mode',copy['CHOOSE_MODE'],'agent','./reaxctl plan --mode localnet --json',copy['PLAN_VERIFY']),
              ('install','Install the pinned kit runtime','agent','./reaxctl install --mode localnet --yes --json','Pinned installation completes'),
              ('localnet','Start the free local chain','agent','./reaxctl localnet up --json','Local chain reports running'),
              ('hotkey','Create the operational hotkey','agent','./reaxctl wallet hotkey --json','Public SS58 address only'),
              ('register','Register with test TAO','agent','./reaxctl register --mode localnet --json','Registered on local chain'),
              ('start','Start the miner','agent','./reaxctl start --json','Process/container health'),
              ('verify','Verify end to end','agent','./reaxctl verify --json','All checklist items pass'),
              ('service','Install the service with approved permissions','agent','./reaxctl service install --json','Service status'),
              ('update-timer','Keep safe updates enabled','agent','./reaxctl update timer install --json','Timer status; manifest changes need approval')]
    steps = [dict(id=i,title=t,who=w,command=c,cost={'kind':'none','note':'Test TAO only; no real payment.'},verify=v,blocked_until_live=False) for i,t,w,c,v in titles]
    mainnet = [dict(s) for s in steps if s['id'] != 'localnet']
    for s in mainnet:
        s['command'] = s['command'].replace('--mode localnet', '--mode mainnet')
        # Global mode is explicit for every real-network command; human approval is still required.
        if '--mode mainnet' not in s['command'] and s['id'] not in ('doctor',):
            s['command'] += ' --mode mainnet'
        if s['id'] == 'choose-mode':
            s['command'] = './reaxctl plan --mode mainnet --json'
        s['blocked_until_live'] = s['id'] not in ('doctor', 'choose-mode')
        s['cost'] = {'kind':'none','note':'No payment by the agent.'}
        if s['id'] == 'install':
            s['command'] += ' --pool s1-fast'
            s['verify'] += '; mainnet requires human-approved --confirm-mainnet'
        if s['id'] == 'register':
            s.update(who='human', title='Human funds and signs registration in their own wallet',cost={'kind':'tao','note':'Live fee, non-refundable burn; human approval required.'}, verify='Correct netuid and public addresses; on-chain registration confirmed')
    at = next(i for i,s in enumerate(mainnet) if s['id']=='register')
    mainnet[at:at] = [dict(id='coldkey', title='Human creates a coldkey on a separate trusted device',who='human',command=None,cost={'kind':'none','note':'No secrets reach the agent.'},verify='Human returns only public SS58 address',blocked_until_live=True),dict(id='coldkeypub',title='Install the public coldkey address',who='agent',command='./reaxctl wallet coldkeypub --ss58 <public-address> --mode mainnet --json',cost={'kind':'none','note':'Public address only'},verify='Public address checksum verified',blocked_until_live=True)]
    for step in steps:
        if STATE == 'prelaunch' and step['id'] not in ('doctor', 'choose-mode'):
            step['command'] = None
            step['verify'] = 'Unavailable until launch; source is private and install exits 12.'
        step['cost']['note'] = 'No payment. Runtime steps open when source is public.' if STATE == 'prelaunch' else 'Test TAO only; no real payment.'
    data = dict(state=STATE, copy=copy, source=release['source'], schema='decisionmodels-mine/1', status=release['status'], updated=lock['updated'], prompts=prompts,
                agent_tiers=[dict(id='A', title='Local execution',capability='Shell/file operations on the selected target host, subject to permissions.', examples=['Claude Code local','Codex CLI local','Cursor local','Gemini CLI local']),dict(id='B',title='Hosted or browser execution',capability='Read guides and prepare a reviewed script; no default target-host shell.',examples=['Cloud coding sessions','Browser agents']),dict(id='C',title='Chat only',capability='Explain and prepare steps; no execution tool.',examples=['Chat without tools'])],rules=rules,steps=steps,mainnet_steps=mainnet,os_support=os_support,requirements=release['requirements'],pools=release['pools'],links=dict(agent='/agent.md',linux='/os/linux',windows='/os/windows',macos='/os/macos',wallets='/wallets',risks='/rewards-and-risks',release='/releases/current.json',kit='https://github.com/fstandhartinger/reax-miner-kit',protocol='https://reax.dev/mine/',faq='https://reax.dev/miner-faq/',register='https://reax.dev/register/'),integrity={k:lock[k] for k in ('version','release_id','commit','sha256','tarball')})
    write('mine.json', json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    prompt_html = '<div class="prompt-card"><div class="prompt-tabs" aria-label="Prompt variants">'
    for ident,label in [('short','Short'),('safe','Safe by default'),('guided',"I’m not technical")]:
        prompt_html += '<button type="button" class="prompt-tab" data-variant="'+ident+'" aria-pressed="'+('true' if ident=='short' else 'false')+'" hidden>'+label+'</button>'
    prompt_html += '</div><div class="prompt-row"><p id="agent-prompt">'+html.escape(prompts['short'])+'</p><button type="button" id="copy-prompt" hidden>Copy prompt</button></div><p class="copy-status" aria-live="polite"></p><noscript><p>Copy the selectable text above into your local coding agent. Read <a href="/agent.md">agent.md</a> first.</p></noscript></div>'
    checker = '''<form class="checker" action="/os/linux" method="get" toolname="check_mining_requirements" tooldescription="Check public REAX OS and GPU requirements and open an OS guide. No actions or wallet access.">
<label for="os">Operating system</label><select id="os" name="os"><option value="linux">Linux</option><option value="windows">Windows</option><option value="macos">macOS</option></select>
<label for="gpu">GPU VRAM</label><select id="gpu" name="gpu"><option value="none">No GPU</option><option value="lt16">NVIDIA &lt;16 GB</option><option value="16">NVIDIA 16–23 GB</option><option value="24">NVIDIA 24–47 GB</option><option value="48">NVIDIA 48+ GB</option><option value="amd">AMD GPU</option><option value="apple">Apple GPU</option></select>
<div class="guide-actions"><button type="submit" formaction="/os/linux" name="guide" value="linux">Linux guide</button><button type="submit" formaction="/os/windows" name="guide" value="windows">Windows guide</button><button type="submit" formaction="/os/macos" name="guide" value="macos">macOS guide</button></div>
<p class="form-note">Without JavaScript, choose your OS guide above.</p></form><div id="verdict" class="verdict" role="status"><strong>{{CHECKER_TITLE}}</strong><p>{{CHECKER_BODY}}</p><a id="os-guide" href="/os/linux">Read the Linux guide →</a></div>'''
    checker = fill(checker)
    diagram = (ROOT/'templates/key-diagram.svg').read_text()
    session_lines = [
        '> Set up this machine for mining at Decision Models by REAX: mine.decisionmodels.io',
        '✓ Read the playbook (agent.md)',
        '✓ Checked hardware: Linux, NVIDIA RTX 4090 · 24 GB',
        '✓ Installed the miner kit (checksum verified)',
        '✓ Rehearsal on a local chain: miner scored 1.000',
        '→ Needs you: create your wallet and approve the registration',
        '  I never see your keys.'
    ]
    if STATE == 'prelaunch':
        session_lines = [session_lines[0], session_lines[1], session_lines[2], '✓ Reviewed hardware, wallet and ports plan', '→ Setup and the free practice run open at launch', '  I stop here until the source is public. Your keys stay with you.']
    session_caption = 'Illustration of a typical session. ' + ('Today: checks and a plan; setup opens at launch.' if STATE == 'prelaunch' else 'Practice with test TAO before real registration.')
    session = '<div class="session-wrap"><div class="agent-session" aria-hidden="true"><div class="session-header"><span class="session-dot"></span>Your agent · this machine<span class="session-tag">LOCAL</span></div><div class="session-transcript">'
    session += ''.join('<p class="session-line line-'+str(i)+'">'+('<span class="session-tick">✓</span>'+html.escape(line[1:]) if line.startswith('✓') else html.escape(line))+'</p>' for i,line in enumerate(session_lines))
    session += '</div></div><p class="visually-hidden">Illustrative agent session: '+html.escape(' '.join(session_lines))+'</p><p class="session-caption">'+session_caption+'</p></div>'
    setup = [
        ('Check hardware', 'Checks your GPU, driver and the requirements.', 'AGENT', '<rect x="4" y="5" width="16" height="12" rx="2"/><path d="M8 21h8M12 17v4M8 9h8M8 13h4"/>'),
        ('Install the kit', 'Installs the pinned miner kit and verifies its checksum.', 'AGENT', '<path d="M12 3v12m-4-4 4 4 4-4M4 16v5h16v-5"/>'),
        ('Create your wallet', 'You create your wallet on a separate trusted device.', 'YOU', '<rect x="3" y="6" width="18" height="15" rx="2"/><path d="M3 9V5l14-2v3M16 12h5v5h-5z"/>'),
        ('Approve registration', ('At launch, you review the fee and sign in your wallet.' if STATE == 'prelaunch' else 'You review the live fee and sign in your own wallet.'), 'YOU', '<path d="M12 3 4 6v6c0 5 8 9 8 9s8-4 8-9V6zM8 12l3 3 5-6"/>'),
        ('Start and verify', 'Starts the miner, checks its answers and keeps it updated.', 'AGENT', '<path d="M4 12a8 8 0 0 1 14-5l2 2M20 3v6h-6M20 12A8 8 0 0 1 6 17l-2-2M4 21v-6h6"/>')
    ]
    if STATE == 'prelaunch':
        setup = [(t, ('At launch: ' + sentence) if t in ('Install the kit', 'Start and verify') else sentence, who, icon) for t,sentence,who,icon in setup]
    timeline = '<ol class="step-cards">'
    for i,(title, sentence, who, icon) in enumerate(setup, 1):
        timeline += '<li class="step-card '+('human-step' if who=='YOU' else '')+'"><div class="step-top"><span class="step-number">0'+str(i)+'</span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+icon+'</svg></div><span class="role-chip '+who.lower()+'">'+who+'</span><h3>'+title+'</h3><p>'+sentence+'</p></li>'
    timeline += '</ol>'
    sample_meta = json.loads((ROOT/'content/samples/provenance.json').read_text())
    if sample_meta['kit_commit'] != lock['commit'] or sample_meta['archive_sha256'] != lock['sha256']:
        raise ValueError('Doctor samples do not match pinned kit; run scripts/make-samples.py')
    doctor = '<div class="doctor-samples"><p class="sample-label">Real output of reaxctl doctor on recorded pre-launch sample machines — not a live miner.</p><div class="doctor-tabs" role="tablist" aria-label="Recorded sample machines">'
    samples = [('4090','24 GB NVIDIA GPU'),('no-gpu','No GPU (hardware check)')]
    for ident,label in samples:
        doctor += '<button type="button" role="tab" id="sample-tab-'+ident+'" data-sample="'+ident+'" aria-selected="'+str(ident=='4090').lower()+'" aria-controls="doctor-'+ident+'" hidden>'+label+'</button>'
    doctor += '</div>'
    doctor_md = 'Real output of reaxctl doctor on recorded pre-launch sample machines — not a live miner.\n\n'
    for ident,label in samples:
        sample=(ROOT/('content/samples/doctor-'+ident+'.txt')).read_text().rstrip()
        doctor += '<div class="doctor-panel" role="tabpanel" aria-labelledby="sample-tab-'+ident+'" id="doctor-'+ident+'"><h3>'+label+'</h3><pre><code>$ ./reaxctl doctor\n'+html.escape(sample)+'</code></pre></div>'
        doctor_md += '### '+label+'\n\n```text\n$ ./reaxctl doctor\n'+sample+'\n```\n\n'
    footnote = 'The 24 GB card qualifies for s1-fast hardware; launch and runtime checks still apply. No-GPU sample shows the source availability note and hardware blockers.'
    doctor += '<p class="sample-footnote">'+footnote+'</p></div>'
    doctor_md += footnote+'\n'
    feature_html = dict(PROMPT_BOX=prompt_html,CHECKER=checker,KEY_DIAGRAM=diagram,DOCTOR=doctor,AGENT_SESSION=session,TIMELINE=timeline)
    feature_md = dict(PROMPT_BOX='\n'.join('### '+k.title()+' prompt\n\n```text\n'+v+'\n```\n' for k,v in prompts.items()),CHECKER='Choose your guide: [Linux](/os/linux) · [Windows](/os/windows) · [macOS](/os/macos). The optional browser checker reads /mine.json.',KEY_DIAGRAM='**Coldkey → your trusted device → funds, approves payments.** Stays home; never crosses to the miner.\n\n**Hotkey → mining machine → signs answers.** No coldkey funds or seed.',DOCTOR=doctor_md,AGENT_SESSION='### Your agent · this machine\n\n```text\n'+'\n'.join(session_lines)+'\n```\n\n'+session_caption,TIMELINE='\n'.join(str(i)+'. **'+who+' · '+title+'** — '+sentence for i,(title,sentence,who,_) in enumerate(setup,1)))
    template = (ROOT/'templates/base.html').read_text()
    sources = {}
    for source in sorted((ROOT/'content').rglob('*.md')):
        rel = source.relative_to(ROOT/'content').with_suffix('').as_posix()
        raw = fill(source.read_text())
        text_source = raw
        for key,value in feature_md.items(): text_source = text_source.replace('{{'+key+'}}',value)
        # Markdown twins use the same words, stripped of presentation wrappers.
        text_source = re.sub(r'</?(?:div|section|details)[^>]*>','',text_source)
        text_source = re.sub(r'<br\s*/?>','\n',text_source)
        text_source = re.sub(r'</?(?:p|summary)[^>]*>','',text_source)
        text_source = re.sub(r' \{#[^}]+\}', '', text_source)
        sources[rel] = text_source
        write(rel+'.md',text_source)
        for key,value in feature_html.items(): raw = raw.replace('{{'+key+'}}',value)
        md = markdown.Markdown(extensions=['extra','toc','md_in_html'],extension_configs={'toc':{'permalink':False}})
        body = md.convert(raw)
        title_match = re.search(r'<h1[^>]*>(.*?)</h1>',body)
        title = re.sub('<[^>]+>','',title_match.group(1)) if title_match else 'Mining guides'
        home = rel == 'index'
        path = '/' if home else '/'+rel
        values = dict(TITLE=html.escape(title),PATH=path,MD_PATH='/'+rel+'.md',CLASS='home' if home else 'docs',LAYOUT='home-layout' if home else 'docs-layout',TOC='' if home else '<aside class="toc" aria-label="On this page"><p class="eyebrow">ON THIS PAGE</p>'+md.toc+'<a href="/'+rel+'.md">Read as Markdown</a></aside>',BODY=body,ROBOTS='index, follow' if INDEXING_ALLOWED else 'noindex, nofollow')
        output = template
        output = fill(output)
        for key,value in values.items(): output=output.replace('{{'+key+'}}',value)
        if re.search(r'\{\{[A-Z_]+\}\}',output+text_source): raise ValueError('Unfilled placeholders in '+rel)
        write(rel+'.html',output)
    write('llms.txt','# Decision Models mining\n\n> Agent-first setup for REAX mining. '+copy['LLMS_NOTE']+'\n\n## Start here\n- [Agent playbook](/agent.md): Canonical instructions and pinned release.\n\n## Guides\n'+''.join('- ['+label+']('+path+'): '+note+'\n' for label,path,note in [('Linux','/os/linux.md','Native host.'),('Windows','/os/windows.md','Conditional WSL2 path.'),('macOS','/os/macos.md','Remote host controller.'),('Wallets','/wallets.md','Custody and human signing.'),('Risks','/rewards-and-risks.md','Variable emissions and costs.'),('Troubleshooting','/troubleshooting.md','Blockers and exit codes.')])+'\n## Machine data\n- [Manifest](/mine.json): Status, steps and rules.\n- [Release](/releases/current.json): Bundled descriptor.\n- [Full guide](/llms-full.txt): Combined Markdown.\n')
    write('llms-full.txt','\n\n---\n\n'.join(sources[k] for k in ['agent','os/linux','os/windows','os/macos','wallets','rewards-and-risks'])+'\n')
    installer = fill((ROOT/'templates/install.sh').read_text()).replace('{{KIT_TARBALL}}',lock['tarball'])
    write('install.sh',installer)
    write('robots.txt','User-agent: *\nAllow: /\n')
    write('.well-known/security.txt','Contact: mailto:info@decisionmodels.io\nExpires: 2027-10-09T00:00:00Z\nCanonical: https://mine.decisionmodels.io/.well-known/security.txt\nPreferred-Languages: en\n')
    config = (ROOT/'nginx.conf').read_text().replace('{{ROBOTS}}','index, follow' if INDEXING_ALLOWED else 'noindex, nofollow')
    write('nginx.conf',config)
    print('Built '+str(len(sources))+' HTML/Markdown pairs; kit '+lock['version']+' '+lock['sha256'])

if __name__ == '__main__': build()

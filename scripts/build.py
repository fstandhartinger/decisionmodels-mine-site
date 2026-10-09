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
        'STATUS_BRIEF': 'REAX is registered on Bittensor Finney mainnet as netuid 92, starting soon. Alpha trading and emission remain disabled until the subnet owner starts it.',
        'SOURCE_STATUS': 'Source and images stay private until launch.',
        'STATUS_PILL': 'Registered · starting soon',
        'STATUS_TITLE': 'Registered as netuid 92, starting soon.',
        'STATUS_BODY': 'REAX is registered on Bittensor Finney mainnet as netuid 92, starting soon. Alpha trading and emission remain disabled until the subnet owner starts it. Source and images stay private until launch. Today your agent can check hardware, wallet and ports; authorized localnet rehearsal remains available to testers with the source. Testnet needs its own configured netuid.',
        'HERO_NOTE': 'Give your coding agent one link. It checks your machine and prepares a safe setup plan for REAX, a peer-to-peer inference network on Bittensor. You keep your keys and approve every payment.',
        'HUMAN_NOTE': 'Your agent can check this machine today. Authorized localnet rehearsal needs REAX_SOURCE_DIR; public setup waits until source and images are published.',
        'STRIP_STATUS': 'Netuid 92 registered · starting soon',
        'PYTHON_NOTE': 'Controller: Python 3.8+; tools virtual environment: Python 3.10+.',
        'PRACTICE_NOTE': 'The subnet is registered as netuid 92 and starting soon; alpha trading and emission remain disabled until the owner starts it. Source and images are private until launch. Run doctor and plan, explain the findings and wallet plan, then stop. Authorized testers can rehearse on localnet with REAX_SOURCE_DIR. Testnet needs its own configured netuid.',
        'META_DESCRIPTION': 'REAX is registered on Bittensor Finney as netuid 92 and starting soon. Check hardware, wallet and ports; source and images stay private until launch.',
        'CHECKER_TITLE': 'Check your machine and prepare for launch.',
        'CHECKER_BODY': 'REAX is registered on Bittensor Finney as netuid 92, starting soon. Alpha trading and emission remain disabled until the owner starts it. Source and images are private until launch; run doctor and plan, then stop. Authorized localnet rehearsal needs REAX_SOURCE_DIR; testnet needs its own configured netuid.',
        'OTHER_HOST': 'Real mining needs another host; prepare your plan today',
        'GPU_NOTE': 'Authorized localnet rehearsal remains available with REAX_SOURCE_DIR; public setup waits until source and images are published.',
        'LLMS_NOTE': 'Registered on Bittensor Finney as netuid 92, starting soon. Alpha trading and emission remain disabled until the owner starts it. Source and images stay private until launch; authorized localnet rehearsal needs REAX_SOURCE_DIR. Testnet needs its own configured netuid.',
        'CHOOSE_MODE': 'Review the preparation plan; source and images stay private until launch',
        'PLAN_VERIFY': 'Explain hardware findings and wallet plan; STOP before install while source and images are private.',
    },
    'live': {
        'STATUS_BRIEF': 'REAX is live on Bittensor Finney mainnet as netuid 92.',
        'SOURCE_STATUS': 'Source and images are public.',
        'STATUS_PILL': 'Network live',
        'STATUS_TITLE': 'The network is open. Practice before registering.',
        'STATUS_BODY': 'The REAX subnet (a network within Bittensor) is live on the main network. Start with a free practice run on a local chain using test TAO (the network’s currency) before real registration. Check the release descriptor for the current netuid; a human approves every payment.',
        'HERO_NOTE': 'Give your coding agent one link. It checks your machine, starts with a free local-chain practice run using test TAO, then prepares real registration. You keep your keys and approve every payment.',
        'HUMAN_NOTE': 'Start with a free practice run using test TAO (the network’s currency) before real registration.',
        'STRIP_STATUS': 'Network live',
        'PYTHON_NOTE': 'Controller: Python 3.8+; tools virtual environment: Python 3.10+.',
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
    # Chain state and source availability are separate launch gates. In particular,
    # chain-live never implies that private source or images can be installed.
    STATE = 'live' if release['status']['live'] else 'prelaunch'
    copy = dict(COPY[STATE])
    netuid = release['status'].get('netuid')
    if netuid is not None:
        for key, value in copy.items():
            copy[key] = value.replace('netuid 92', 'netuid ' + str(netuid))
    if STATE == 'live' and not release['source']['public']:
        copy.update(STATUS_BRIEF='REAX is live on Bittensor Finney as netuid '+str(netuid)+'.',
                    SOURCE_STATUS='The chain is live, but source and images remain private until separately published.',
                    STATUS_BODY='The REAX subnet is live on Bittensor Finney as netuid '+str(netuid)+', but miner source and images remain private. Alpha trading and epochs have started; TAO rewards depend on the separate root-gated subnet emission flag and can be zero. Public setup and rehearsal stay blocked until the source and images are published. Authorized localnet rehearsal needs REAX_SOURCE_DIR. Testnet needs its own configured netuid.',
                    PRACTICE_NOTE='The network is live as netuid '+str(netuid)+', but source and images are still private. Stop after doctor and plan; install and localnet rehearsal require public source, or an authorized REAX_SOURCE_DIR for localnet. Testnet needs its own configured netuid.',
                    HUMAN_NOTE='The network is live as netuid '+str(netuid)+'; source and images are private, so setup remains gated.',
                    CHECKER_BODY='Bittensor Finney is live as netuid '+str(netuid)+', but source and images remain private. Run doctor and plan, then stop. Localnet rehearsal requires public source or an authorized REAX_SOURCE_DIR; testnet needs its own configured netuid.',
                    STRIP_STATUS='Network live · netuid '+str(netuid)+' · source private', STATUS_PILL='Network live',
                    STATUS_TITLE='Network live as netuid '+str(netuid)+'. Source remains private.',
                    HERO_NOTE='Give your coding agent one link. It checks your machine and prepares a plan; source and images remain private, so public setup is still gated. You keep your keys and approve every payment.',
                    LLMS_NOTE='Bittensor Finney is live as netuid '+str(netuid)+', but source and images stay private. Stop after doctor and plan; authorized localnet rehearsal needs REAX_SOURCE_DIR. Testnet needs its own configured netuid.',
                    CHOOSE_MODE='Review the plan; source and images remain private',
                    PLAN_VERIFY='Explain host findings; STOP before install because source and images are private.')
    elif STATE == 'prelaunch' and release['source']['public']:
        copy.update(STATUS_BRIEF='REAX source is public; Bittensor Finney registration is starting soon as netuid '+str(netuid)+'. Alpha trading and emission remain disabled until the subnet owner starts it.',
                    SOURCE_STATUS='Source is public; container images remain private until launch.',
                    STATUS_PILL='Practice run available', STATUS_TITLE='Practice on localnet while the network starts.',
                    STATUS_BODY='The REAX source is public, so a free localnet rehearsal with test TAO is available. Bittensor Finney registration remains starting soon as netuid '+str(netuid)+'; alpha trading and emission remain disabled until the subnet owner starts it. Mainnet stays blocked until status.live is true and images are public. Testnet needs its own configured netuid.',
                    HERO_NOTE='Give your coding agent one link. It can check this machine and rehearse locally with test TAO; mainnet setup waits until the network and images are ready. You keep your keys and approve every payment.',
                    HUMAN_NOTE='Your agent can start a free localnet rehearsal. Mainnet is still starting soon as netuid '+str(netuid)+'.',
                    STRIP_STATUS='Netuid '+str(netuid)+' registered · practice available',
                    CHECKER_BODY='Localnet rehearsal with test TAO is available because source is public. Mainnet is registered as netuid '+str(netuid)+' and remains blocked until status.live is true.',
                    LLMS_NOTE='Practice free on localnet with test TAO because source is public. Mainnet is registered as netuid '+str(netuid)+' and remains blocked until status.live is true.',
                    CHOOSE_MODE='Choose a free localnet rehearsal before real registration',
                    PLAN_VERIFY='Review the ordered localnet practice plan; mainnet remains blocked while starting soon.')
    if release['source']['public'] and not release.get('images', {}).get('public', False):
        copy['SOURCE_STATUS'] = 'Source is public; container images remain private until published.'
    # Live chain copy still reflects image visibility; private images block real setup.
    if STATE == 'live' and not release.get('images', {}).get('public', False):
        copy['STATUS_BODY'] += ' Container images remain private too; mainnet installation stays blocked until they are published.'
    if STATE == 'live' and release['source']['public']:
        copy.update(STRIP_STATUS='Network live · netuid '+str(netuid), STATUS_TITLE='The network is live as netuid '+str(netuid)+'.')
    # Source publication permits rehearsal, but never by itself marks the network live.
    if STATE == 'prelaunch' and release['source']['public']:
        copy.update(STRIP_STATUS='Not live yet — practice available', STATUS_PILL='Practice run available', STATUS_TITLE='Practice before launch.',
                    HUMAN_NOTE='Your agent can start a free practice run today. Mainnet registration remains blocked until status.live is true.',
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
    mainnet_ready = bool(release['status']['live'] and release['source']['public'] and release.get('images', {}).get('public', False))
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
    substitutions = {'KIT_VERSION': lock['version'], 'RELEASE_ID': lock['release_id'], 'KIT_COMMIT': lock['commit'], 'KIT_SHA256': lock['sha256'], 'UPDATED': lock['updated']}
    substitutions.update(copy)
    def fill(value):
        for key, replacement in substitutions.items():
            value = value.replace('{{' + key + '}}', replacement)
        return value
    prompts = {k: fill(v) for k,v in json.loads((ROOT / 'content/prompts.json').read_text()).items()}
    live_short = prompts.pop('short_live')  # offer setup only when source is actually public
    if STATE == 'live' and release['source']['public'] and release.get('images', {}).get('public', False):
        prompts['short'] = live_short
    rules = [
        'Never ask for, read, print, log, store or transmit a recovery phrase or coldkey private file.',
        'Only public addresses and the operational hotkey belong on the mining machine. Never display hotkey contents.',
        'A human approves every payment and signs registration; never buy TAO, rent hardware or fund accounts.',
        'Ask before admin, firewall or router changes. Never publish ports 8101, 8102 or 8000.',
        'Default to localnet. Mainnet setup requires status.live, source.public, images.public and human-approved --confirm-mainnet.',
        'Testnet requires status.live, public source and images, and its own configured status.testnet_netuid. Never infer or reuse the Finney mainnet netuid for testnet.',
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
    all_steps = [dict(id=i,title=t,who=w,command=c,cost={'kind':'none','note':'Test TAO only; no real payment.'},verify=v,blocked_until_live=False) for i,t,w,c,v in titles]
    mainnet = [dict(s) for s in all_steps if s['id'] != 'localnet']
    steps = [s for s in all_steps if s['id'] not in ('service', 'update-timer')]  # persistent units make no sense for a throw-away practice chain
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
            s['command'] += ' --pool s1-fast --confirm-mainnet'
            s['verify'] += '; mainnet requires human-approved --confirm-mainnet'
        if s['id'] == 'register':
            s.update(who='human', title='Human funds and signs registration in their own wallet',cost={'kind':'tao','note':'Live fee, non-refundable burn; human approval required.'}, verify='Correct netuid and public addresses; on-chain registration confirmed')
    at = next(i for i,s in enumerate(mainnet) if s['id']=='register')
    mainnet[at:at] = [dict(id='coldkey', title='Human creates a coldkey on a separate trusted device',who='human',command=None,cost={'kind':'none','note':'No secrets reach the agent.'},verify='Human returns only public SS58 address',blocked_until_live=True),dict(id='coldkeypub',title='Install the public coldkey address',who='agent',command='./reaxctl wallet coldkeypub --ss58 <public-address> --mode mainnet --json',cost={'kind':'none','note':'Public address only'},verify='Public address checksum verified',blocked_until_live=True)]
    for step in steps:
        if not release['source']['public'] and step['id'] not in ('doctor', 'choose-mode'):
            step['blocked_until_live'] = True
            step['verify'] = 'Unavailable to the public while source is private; install exits 12. Authorized localnet rehearsal may use REAX_SOURCE_DIR.'
        step['cost']['note'] = 'No payment. Localnet rehearsal requires public source or an authorized REAX_SOURCE_DIR.' if not release['source']['public'] else 'Test TAO only; no real payment.'
    for step in mainnet:
        step['blocked_until_live'] = not mainnet_ready and step['id'] not in ('doctor', 'choose-mode')
        if not mainnet_ready:
            if step['id'] not in ('doctor', 'choose-mode'):
                step['verify'] = 'Unavailable until the network is live and source and images are public; registration remains a human payment and signing step.'
            step['cost']['note'] = 'No payment by the agent.'
    data = dict(state=STATE, copy=copy, source=release['source'], schema='decisionmodels-mine/1', status=release['status'], updated=lock['updated'], prompts=prompts,
                agent_tiers=[dict(id='A', title='Local execution',capability='Shell/file operations on the selected target host, subject to permissions.', examples=['Claude Code local','Codex CLI local','Cursor local','Gemini CLI local']),dict(id='B',title='Hosted or browser execution',capability='Read guides and prepare a reviewed script; no default target-host shell.',examples=['Cloud coding sessions','Browser agents']),dict(id='C',title='Chat only',capability='Explain and prepare steps; no execution tool.',examples=['Chat without tools'])],rules=rules,steps=steps,mainnet_steps=mainnet,os_support=os_support,requirements=release['requirements'],pools=release['pools'],links=dict(agent='/agent.md',linux='/os/linux',windows='/os/windows',macos='/os/macos',wallets='/wallets',risks='/rewards-and-risks',release='/releases/current.json',kit='https://github.com/reaxlabs/reax-miner-kit',protocol='https://reax.dev/mine/',faq='https://reax.dev/miner-faq/',register='https://reax.dev/register/'),integrity={k:lock[k] for k in ('version','release_id','commit','sha256','tarball')})
    write('mine.json', json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    prompt_html = '<div class="prompt-card"><div class="prompt-tabs" role="tablist" aria-label="Prompt variants">'
    for ident,label in [('short','Short'),('safe','Safe by default'),('guided',"I’m not technical")]:
        prompt_html += '<button type="button" class="prompt-tab" data-variant="'+ident+'" id="prompt-tab-'+ident+'" role="tab" aria-controls="agent-prompt" tabindex="'+('0' if ident=='short' else '-1')+'" aria-selected="'+('true' if ident=='short' else 'false')+'" hidden>'+label+'</button>'
    prompt_html += '</div><div class="prompt-row"><p id="agent-prompt" role="tabpanel" aria-labelledby="prompt-tab-short" aria-live="polite">'+html.escape(prompts['short'])+'</p><button type="button" id="copy-prompt" hidden>Copy prompt</button></div><p class="copy-status" aria-live="polite"></p><noscript><p>Copy the selectable text above into your local coding agent. Read <a href="/agent.md">agent.md</a> first.</p></noscript></div>'
    checker = '''<form hidden class="checker" action="/os/linux" method="get" toolname="check_mining_requirements" tooldescription="Check public REAX OS and GPU requirements and open an OS guide. No actions or wallet access.">
<label for="os">Operating system</label><select id="os" name="os"><option value="">Choose…</option><option value="linux">Linux</option><option value="windows">Windows</option><option value="macos">macOS</option></select>
<label for="gpu">GPU memory (VRAM)</label><select id="gpu" name="gpu"><option value="">Choose…</option><option value="none">No GPU</option><option value="lt16">NVIDIA &lt;16 GB</option><option value="16">NVIDIA 16–23 GB</option><option value="24">NVIDIA 24–47 GB</option><option value="48">NVIDIA 48+ GB</option><option value="amd">AMD GPU</option><option value="apple">Apple GPU</option></select>
<div class="guide-actions"><button type="submit" formaction="/os/linux" name="guide" value="linux">Linux guide</button><button type="submit" formaction="/os/windows" name="guide" value="windows">Windows guide</button><button type="submit" formaction="/os/macos" name="guide" value="macos">macOS guide</button></div>
</form><div id="verdict" class="verdict" role="status" hidden></div><noscript><form class="guide-actions" action="/os/linux"><button type="submit" formaction="/os/linux">Linux guide</button><button type="submit" formaction="/os/windows">Windows guide</button><button type="submit" formaction="/os/macos">macOS guide</button></form></noscript>'''
    checker = fill(checker)
    diagram = (ROOT/'templates/key-diagram.svg').read_text()
    session_lines = [
        '> ' + ('Set up this machine for mining at Decision Models by REAX: mine.decisionmodels.io' if mainnet_ready else 'Check this computer for REAX mining: mine.decisionmodels.io'),
        '✓ Read the playbook (agent.md)',
        '✓ Checked hardware: Linux, NVIDIA RTX 4090 · 24 GB',
        '✓ Installed the miner kit (checksum verified)',
        '✓ Rehearsal on a local chain: miner scored 1.000',
        '→ Needs you: create your wallet and approve registration. I never see your keys.'
    ]
    if not mainnet_ready and not release['source']['public']:
        session_lines = [session_lines[0], session_lines[1], session_lines[2], '✓ Reviewed hardware, wallet and ports plan', '→ Public setup waits until source and images are published', '  Authorized localnet rehearsal needs REAX_SOURCE_DIR.']
    elif not mainnet_ready:
        session_lines = [session_lines[0], session_lines[1], session_lines[2], '✓ Rehearsed on localnet with test TAO', '→ Mainnet setup waits for the network, source and images', '  Testnet requires its own configured netuid.']
    session_caption = 'Illustration of a typical session. ' + ('Practice with test TAO before mainnet setup.' if release['source']['public'] else 'Checks and plan; authorized localnet rehearsal needs REAX_SOURCE_DIR.')
    session = '<div class="session-wrap"><div class="agent-session" aria-hidden="true"><div class="session-header"><span class="session-dot"></span>Your agent · this machine<span class="session-tag">LOCAL</span></div><div class="session-transcript">'
    session += ''.join('<p class="session-line line-'+str(i)+'">'+('<span class="session-tick">✓</span>'+html.escape(line[1:]) if line.startswith('✓') else html.escape(line))+'</p>' for i,line in enumerate(session_lines))
    session += '</div></div><p class="visually-hidden">Illustrative agent session: '+html.escape(' '.join(session_lines))+'</p><p class="session-caption">'+session_caption+'</p></div>'
    setup = [
        ('Check hardware', 'Checks your GPU, driver and the requirements.', 'AGENT', '<rect x="4" y="5" width="16" height="12" rx="2"/><path d="M8 21h8M12 17v4M8 9h8M8 13h4"/>'),
        ('Install the kit', 'Installs the pinned miner kit and verifies its checksum.', 'AGENT', '<path d="M12 3v12m-4-4 4 4 4-4M4 16v5h16v-5"/>'),
        ('Create your wallet', 'You create your wallet on a separate trusted device.', 'YOU', '<rect x="3" y="6" width="18" height="15" rx="2"/><path d="M3 9V5l14-2v3M16 12h5v5h-5z"/>'),
        ('Approve registration', ('When mainnet setup opens, you review the live fee and sign in your wallet.' if not mainnet_ready else 'You review the live fee and sign in your own wallet.'), 'YOU', '<path d="M12 3 4 6v6c0 5 8 9 8 9s8-4 8-9V6zM8 12l3 3 5-6"/>'),
        ('Start and verify', 'Starts the miner, checks its answers and keeps it updated.', 'AGENT', '<path d="M4 12a8 8 0 0 1 14-5l2 2M20 3v6h-6M20 12A8 8 0 0 1 6 17l-2-2M4 21v-6h6"/>')
    ]
    if not mainnet_ready:
        setup = [(t, ('When mainnet setup opens: ' + sentence) if t in ('Install the kit', 'Start and verify') else sentence, who, icon) for t,sentence,who,icon in setup]
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
        raw = source.read_text()
        if rel != 'agent':
            raw = raw.replace('{{PRACTICE_NOTE}}', '{{HUMAN_NOTE}}')
        raw = fill(raw)
        text_source = raw
        for key,value in feature_md.items(): text_source = text_source.replace('{{'+key+'}}',value)
        # Markdown twins use the same words, stripped of presentation wrappers.
        text_source = re.sub(r'</?(?:div|section|details)\b[^>]*>','',text_source)
        text_source = re.sub(r'<br\s*/?>','\n',text_source)
        text_source = re.sub(r'</?(?:p|summary)\b[^>]*>','',text_source)
        text_source = re.sub(r' \{#[^}]+\}', '', text_source)
        sources[rel] = text_source
        write(rel+'.md',text_source)
        for key,value in feature_html.items(): raw = raw.replace('{{'+key+'}}',value)
        md = markdown.Markdown(extensions=['extra','toc','md_in_html'],extension_configs={'toc':{'permalink':False}})
        body = md.convert(raw)
        body = body.replace('<table>', '<div class="table-scroll" tabindex="0" role="region" aria-label="Table"><table>').replace('</table>', '</table></div>')
        title_match = re.search(r'<h1[^>]*>(.*?)</h1>',body)
        title = re.sub('<[^>]+>','',title_match.group(1)) if title_match else 'Mining guides'
        home = rel == 'index'
        path = '/' if home else '/'+rel
        values = dict(TITLE=html.escape(title),PATH=path,MD_PATH='/'+rel+'.md',CLASS='home' if home else 'docs',LAYOUT='home-layout' if home or rel == '404' else 'docs-layout',TOC='' if home or rel == '404' else '<aside class="toc" aria-label="On this page"><p class="eyebrow">ON THIS PAGE</p>'+md.toc+'<a href="/'+rel+'.md">Read as Markdown</a></aside>',BODY=body,ROBOTS='index, follow' if INDEXING_ALLOWED else 'noindex, nofollow')
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
    write('.well-known/security.txt','Contact: mailto:info@productivity-boost.com\nExpires: 2027-10-09T00:00:00Z\nCanonical: https://mine.decisionmodels.io/.well-known/security.txt\nPreferred-Languages: en\n')
    config = (ROOT/'nginx.conf').read_text().replace('{{ROBOTS}}','index, follow' if INDEXING_ALLOWED else 'noindex, nofollow')
    write('nginx.conf',config)
    print('Built '+str(len(sources))+' HTML/Markdown pairs; kit '+lock['version']+' '+lock['sha256'])

if __name__ == '__main__': build()

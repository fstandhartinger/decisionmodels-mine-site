<div class="hero" markdown="1">
<div class="hero-copy" markdown="1">
<p class="eyebrow">BITTENSOR SUBNET 92 · REAX · DECISION MODELS</p>

# Point your agent here. Mine with your own GPU.

<p class="lead">{{HERO_NOTE}}</p>

{{PROMPT_BOX}}

<div class="requirements-strip"><span>NVIDIA GPU · 24 GB+ (RTX 3090/4090/5090 and up)</span><span>Linux (Windows via WSL2 is conditional)</span><span class="status-pill">{{STRIP_STATUS}}</span></div>

<p class="compatibility">A coding agent is an AI tool that can run commands on the computer you authorize. Tested with Claude Code; other coding agents that can run commands on your computer may work, but we have not tested them. <a href="/wallets#glossary">New to coding agents? Start here.</a></p>

<p class="agent-note">AI agent reading this page? The complete playbook is <a href="/agent.md">/agent.md</a> (also <a href="/llms-full.txt">/llms-full.txt</a>): status, hardware verdicts, rental prices, wallet without seeds, rewards and converting, and the EU miner track. The quick answers below summarise it.</p>

[Prefer to do it yourself? Read the playbook →](/agent)
</div>

{{AGENT_SESSION}}
</div>

<section class="honest" id="status" aria-labelledby="status-title" markdown="1">
<p class="eyebrow">HONEST STATUS</p>

## {{STATUS_TITLE}} {#status-title}

{{STATUS_BODY}}
</section>

<section class="home-section" id="quick-answers" markdown="1">
<p class="eyebrow">QUICK ANSWERS</p>

## The short version

| Question | Answer |
| --- | --- |
| Can my computer mine? | Yes with **one NVIDIA GPU of 24 GB or more** (RTX 3090, 4090, 5090, A6000, L40S, A100, H100, H200, B200, B300 …), driver R580+, Linux (Windows via WSL2 is conditional). **No** with 16 GB or less (most laptops), Apple, AMD, Intel or no GPU. Smaller quantised builds are not accepted. [Hardware details](/hardware) |
| No suitable GPU? | Rent one with Docker and a reachable port, for example a Lium RTX 3090/4090 pod (from about $0.20–0.55 per hour, payable in TAO too), Scaleway L40S in Paris (about €1.40 per hour) or a Hetzner GPU server in Germany (from €889 per month); prices checked 12 October 2026. [All options](/rent) |
| Which wallet? | Create the coldkey yourself, never through an agent: the **Talisman** browser extension (Polkadot/Substrate account) or **btcli** on your own computer (`btcli wallet new-coldkey`). Only the public address (starts with 5) goes to your agent; the miner's hotkey is created on the mining server. [Wallets](/wallets) |
| How are rewards paid? | Validators test each miner every round; the chain shares the subnet's emission by score and pays miners in the subnet's token (alpha), credited as stake on the miner's hotkey. Variable, can be zero, and only once emissions run. [Rewards](/rewards-and-risks) |
| How do I get euros? | Unstake alpha to TAO (`btcli stake remove --netuid 92`, a pool swap with slippage), send TAO to an exchange that lists TAO and is authorised in your country, sell for EUR and withdraw. Fees and taxes apply. You can also keep your alpha staked to a validator; staked alpha takes part in validator emissions under the protocol rules. Whether you keep, stake or convert is your own decision; this is not financial or tax advice. [Step by step](/rewards-and-risks#what-you-can-do-with-earned-alpha) |
| We are an EU company | Sign the sub-processing agreement (AVV, Art. 28 GDPR) online at [/eu/sign](/eu/sign); requirements and EU AI Act notes on [/eu](/eu). |
| I use an AI coding agent | Point it at [/agent.md](/agent.md): the complete playbook with hardware verdicts, setup commands, wallet rules and the EU track. |
</section>

<section class="home-section" markdown="1">
<p class="eyebrow">01 / THE SETUP</p>

## What happens

{{TIMELINE}}

{{PRACTICE_NOTE}}

{{DOCTOR}}

</section>

<section class="home-section" id="requirements" markdown="1">
<p class="eyebrow">02 / YOUR MACHINE</p>

## Will my computer work?

{{CHECKER}}

The fast pool serves a small 4-billion-parameter model, so a single **24 GB NVIDIA card** such as an RTX 3090, 4090 or 5090 is enough. Your agent checks the exact GPU, driver, container, model and network. [Which cards work, measured speeds and why there is no low-precision mode →](/hardware)

| Component | Requirement |
| --- | --- |
| GPU | One NVIDIA GPU with ≥24 GB VRAM (GPU memory); one GPU per miner |
| Driver | R580+ for CUDA 13 |
| Host | 4 CPU cores · 32 GB RAM · 20 GB free disk |
| Network | Public IP · inbound TCP 8091 · synchronized clock |
| OS | Linux x86_64; Windows via WSL2 is conditional and not yet tested by us end to end |

No suitable GPU? Rent one by the hour; your agent compares options with you. [Rent a GPU →](/rent)
</section>

<section class="home-section keys-section" markdown="1">
<div class="keys-copy" markdown="1">
<p class="eyebrow">03 / YOUR KEYS</p>

## You keep the keys

- Your coldkey (the key controlling your funds) stays on a separate trusted device.
- The agent never sees your recovery phrase or coldkey private file.
- A human approves every payment.

[New to mining? Read the glossary →](/wallets#glossary)

[Choose a wallet and understand the signing boundary →](/wallets)
</div>

{{KEY_DIAGRAM}}
</section>

<section class="home-section risks" markdown="1">
<p class="eyebrow">04 / A CLEAR VIEW</p>

## Rewards and risks

Validators test every miner each round and score answers that match their reference run. The chain shares the subnet's emission by those scores; miners receive the subnet's token (alpha). Rewards start when emissions start, vary, and can be zero. Hardware, electricity, connection and a non-refundable registration burn are your costs.

The planned norm is about 80 % of miner emissions for serving inference and about 20 % for competitions (such as a faster REAX Engine, not live yet). The split can change, for example with more for competitions while paid inference demand ramps up; changes are announced in advance on this site and reax.co, with their start date.

[How rewards arise, how they are split, converting to TAO or euros, and the risks →](/rewards-and-risks)
</section>

<section class="home-section" id="eu" markdown="1">
<p class="eyebrow">05 / FOR COMPANIES</p>

## EU miners: mining under a GDPR sub-processing agreement

EU companies with GPUs in EU data centres can sign a sub-processing agreement (AVV, Art. 28 GDPR) online. Once verified, a company may serve Decision Models' EU-tier traffic in addition to normal mining. EU routing is switched off until the first verified EU miner, and no traffic volume is promised. Requirements, EU AI Act notes and the signing flow are on one page.

[EU miner track →](/eu) · [Sign the agreement →](/eu/sign)
</section>

<section class="home-section" markdown="1">
<p class="eyebrow">06 / MACHINE ENTRY POINTS</p>

## For agents

| Entry point | What it gives you |
| --- | --- |
| [agent.md](/agent.md) | Canonical playbook, approvals and pinned commands |
| [llms.txt](/llms.txt) | A short map of the docs |
| [hardware.md](/hardware.md) | Pools, minimum GPUs, measured speeds |
| [rent.md](/rent.md) | GPU rental options with dated prices |
| [eu.md](/eu.md) | EU (GDPR) miner track and AVV signing |
| [mine.json](/mine.json) | Status, steps, requirements and rules |
| [releases/current.json](/releases/current.json) | The kit's bundled release descriptor |
| [install.sh](/install.sh) | Readable pinned-archive download; read before running |
| [Kit source](https://github.com/reaxlabs/reax-miner-kit) | Review the Python commands |
| [WebMCP tools](/webmcp) | Optional read-only tools; browser support varies |

Local agents can act on the selected machine. Cloud/browser agents can prepare a plan; chat-only agents can explain steps. The agent must say where its commands run. WebMCP does not grant a local shell or permission to spend.

<p class="integrity">Kit {{KIT_VERSION}} · subnet release {{RELEASE_ID}}<br>commit {{KIT_COMMIT}}<br>SHA-256 {{KIT_SHA256}}</p>
</section>

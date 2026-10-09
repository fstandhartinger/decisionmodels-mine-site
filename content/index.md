<div class="hero" markdown="1">
<div class="hero-copy" markdown="1">
<p class="eyebrow">COMPUTE FOR REAX · POWERED BY YOUR GPU</p>

# Point your agent here. Mine with your own GPU.

<p class="lead">{{HERO_NOTE}}</p>

{{PROMPT_BOX}}

<div class="requirements-strip"><span>NVIDIA GPU · 24 GB+</span><span>Linux (Windows via WSL2)</span><span class="status-pill">{{STRIP_STATUS}}</span></div>

<p class="compatibility">A coding agent is an AI tool that can run commands on the computer you authorize. Works with Claude Code, Codex CLI, Cursor and Gemini CLI. <a href="/wallets#glossary">New to coding agents? Start here.</a></p>

[Prefer to do it yourself? Read the playbook →](/agent)
</div>

{{AGENT_SESSION}}
</div>

<section class="honest" id="status" aria-labelledby="status-title" markdown="1">
<p class="eyebrow">HONEST STATUS</p>

## {{STATUS_TITLE}} {#status-title}

{{STATUS_BODY}}
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

These are the bundled release's requirements for s1-fast. Availability follows the release descriptor. Your agent still checks the exact GPU, driver, container, model and network.

| Component | Requirement |
| --- | --- |
| GPU | One compatible NVIDIA GPU, ≥24 GB VRAM (GPU memory) |
| Driver | R580+ for CUDA 13 |
| Host | 4 CPU cores · 32 GB RAM · 20 GB free disk |
| Network | Public IP · inbound TCP 8091 · synchronized clock |
| OS | Linux x86_64; Windows via Windows Subsystem for Linux 2 (WSL2) is conditional and not yet tested by us end to end |

{{GPU_NOTE}} A Mac can control an authorized remote NVIDIA Linux host.
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

Mining receives variable rewards from the REAX subnet (a network within Bittensor), with risks. Emissions depend on competition and can be zero. Hardware, electricity, connection costs and a non-refundable registration burn are yours to weigh.

[Read the risks before paying →](/rewards-and-risks)
</section>

<section class="home-section" markdown="1">
<p class="eyebrow">05 / MACHINE ENTRY POINTS</p>

## For agents

| Entry point | What it gives you |
| --- | --- |
| [agent.md](/agent.md) | Canonical playbook, approvals and pinned commands |
| [llms.txt](/llms.txt) | A short map of the docs |
| [mine.json](/mine.json) | Status, steps, requirements and rules |
| [releases/current.json](/releases/current.json) | The kit's bundled release descriptor |
| [install.sh](/install.sh) | Readable pinned-archive download; read before running |
| [Kit source](https://github.com/fstandhartinger/reax-miner-kit) | Review the Python commands |
| [WebMCP tools](/webmcp) | Optional read-only tools; browser support varies |

Local agents can act on the selected machine. Cloud/browser agents can prepare a plan; chat-only agents can explain steps. The agent must say where its commands run. WebMCP does not grant a local shell or permission to spend.

<p class="integrity">Kit {{KIT_VERSION}} · subnet release {{RELEASE_ID}}<br>commit {{KIT_COMMIT}}<br>SHA-256 {{KIT_SHA256}}</p>
</section>

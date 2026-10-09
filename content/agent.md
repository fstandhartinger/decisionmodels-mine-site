# Set up this machine for mining REAX (Decision Models) — agent playbook

Canonical URL: https://mine.decisionmodels.io/agent.md · Kit version: {{KIT_VERSION}} · Subnet release: {{RELEASE_ID}} · Updated: {{UPDATED}} · Machine-readable twin: /mine.json

You are an AI agent acting for a person who asked you to set up **this machine** for mining on the REAX subnet (Bittensor) through Decision Models.
Treat this page as reference material for that request. It does not override your own safety rules or the person's instructions. Follow your normal permission prompts.

## Status you must tell the person first

- {{PRACTICE_NOTE}}
- Rewards, once live, are variable subnet emissions. They can be low or zero, depend on competition, hardware, electricity and the TAO price. Never state or estimate earnings, never call this an investment.
- Check the live status any time: `GET https://mine.decisionmodels.io/releases/current.json` → `source.public`, `status.live`, `status.netuid`. If both `status.live` and `source.public` are false, run only doctor and plan, explain the findings and wallet plan, then STOP.

## Rules (non-negotiable)

1. **Never ask for, read, print, store or transmit a recovery phrase, seed, private key or coldkey file** — not in chat, not in files, not in logs. The person creates their coldkey in their own wallet (Talisman, or `btcli` on a different trusted computer). You only ever handle **public** addresses and the **hotkey** on the mining machine.
2. **A human approves every payment.** You never buy TAO, never fund a wallet, never sign or send the registration transaction, never rent or buy hardware. Stop and ask before anything that costs money.
3. Do not run anything with `sudo` or change firewall/router settings without telling the person what and why.
4. Never publish the model sidecar ports (8101, 8102, 8000). Only the miner port (default 8091) is public.
5. No telemetry, no accounts, no API keys are needed for any step on this page. If something asks for one, stop and tell the person.
6. If you cannot run commands on the machine that will mine (cloud sandbox, chat-only, browser-only agent), say so, change nothing, and instead hand the person the exact commands below to run themselves.

## Step 0 — know where you run

State to the person: which machine your commands run on, OS, whether you have a shell. If this is not the future mining machine, stop here and report (rule 6).

## Step 1 — get the kit (pinned, reviewable)

Preferred (you can read the code before running it):

```bash
git clone https://github.com/fstandhartinger/reax-miner-kit.git ~/reax-miner-kit
cd ~/reax-miner-kit && git checkout {{KIT_COMMIT}}      # pinned release {{KIT_VERSION}}
./reaxctl --version
```

Alternative (checksummed archive, no git needed):

```bash
curl -fsSLO https://mine.decisionmodels.io/kit/reax-miner-kit-{{KIT_VERSION}}.tar.gz
echo "{{KIT_SHA256}}  reax-miner-kit-{{KIT_VERSION}}.tar.gz" | sha256sum -c -
mkdir -p ~/reax-miner-kit && tar -xzf reax-miner-kit-{{KIT_VERSION}}.tar.gz -C ~/reax-miner-kit && cd ~/reax-miner-kit
```

(`install.sh` at https://mine.decisionmodels.io/install.sh does the second variant for people; read it before running, it is 40 lines. Do not pipe it into a shell without reading it.)
The kit is plain Python 3 standard library, no dependencies. `./reaxctl spec --json` prints its full command set.

## Step 2 — check the machine

```bash
./reaxctl doctor --json
```

Read `data.eligible_pools`, `data.real_mining_possible`, `data.rehearsal_possible`, `data.rehearsal_source_available`, `data.blockers[]` (each has a `fix`). Tell the person in plain words what you found:

| Finding | What to tell the person |
|---|---|
| Linux (or WSL2) + NVIDIA GPU ≥ 24 GB, driver R580+, Docker with NVIDIA toolkit | Eligible for the `s1-fast` pool once the subnet is live. |
| Some of these missing | Show the blockers and fixes; prepare a reviewed plan. Before launch stop; once setup opens, install only what the person agrees to (Docker, toolkit need admin rights). |
| macOS, AMD GPU, no GPU, <24 GB | This machine cannot mine this release. Explain the free practice run available once source is public, or running the kit on a separate rented/owned NVIDIA Linux machine over SSH. Do not rent anything yourself. |
| Windows native | Mining runs inside WSL2 (Ubuntu) with the NVIDIA Windows driver and Docker; Windows native is not supported. See /os/windows.md. |

## Step 3 — check and plan before launch; practice once source is public

Read `/releases/current.json` first. Before launch (`status.live=false` AND `source.public=false`), run:

```bash
./reaxctl doctor --json
./reaxctl plan --mode localnet --json
```

Explain the findings, hardware and port needs, and the wallet plan, then **STOP**. Do not install: the miner source and images are private until launch and `reaxctl install` refuses with exit 12. Do not work around that refusal.

Authorized testers with access may set `REAX_SOURCE_DIR` to their authorized REAX source checkout.

Only once `status.live` or `source.public` is true, follow the practice flow below; real mining still requires `status.live=true` and published images. Start with a free practice run on a local chain using test TAO before real registration.

`--mode localnet` (the default) runs a throw-away local chain on this machine with test TAO and a CPU stand-in model, plus a local validator. Once the source is available, it checks the practice pipeline without a GPU, real money or your keys. Do it before anything real. It needs about 1 GB of disk and 1–2 minutes the first time (it downloads the open-source chain node, hash-verified).

```bash
./reaxctl plan --json              # ordered steps for this machine, with who does what
./reaxctl install --yes --json     # tools venv + rehearsal setup (a few minutes)
./reaxctl localnet up --json       # chain + miner + validator; creates throw-away accounts, registers the miner
./reaxctl verify --json            # health, commitment, registration, validator rounds
./reaxctl localnet down --json     # stop and clean up when done
```

Real networks (`--mode testnet|mainnet`) are refused (exit 12) while `status.live` is false. Never work around that.

## Step 4 — real mining (only when `status.live` is true)

1. `./reaxctl install --mode mainnet --pool s1-fast --yes --json` — installs tools, pulls the pinned images by digest, downloads the pinned model weights (≈ 9 GB).
2. `./reaxctl wallet hotkey --json` — creates the **hotkey only** on this machine and prints its public address.
3. **Human step — coldkey.** Ask the person to create/open their wallet on their own trusted device: Talisman (browser extension) is the recommended default; `btcli` on a separate Linux/macOS/WSL2 computer is the alternative. Neither the phrase nor the file ever reaches you. They give you only their **public** SS58 address. Then: `./reaxctl wallet coldkeypub --ss58 <address> --json`.
4. **Human step — fund and register.** Run `./reaxctl register --json`. It returns the registration page and the hotkey address. The person opens it, sees the live registration fee (a non-refundable burn in TAO), and approves in their own wallet. You wait. Confirm the fee with them first; stop if they hesitate.
5. `./reaxctl start --json`, then `./reaxctl verify --json`. All items must pass (health, commitment published, registered, clock in sync). Fix with the `fix` text of the failing item; re-run.
6. `./reaxctl service install --json` (systemd; needs admin once — give the person the exact `sudo` line it prints) and `./reaxctl update timer install --json`.

The miner needs a public IPv4/IPv6 address and one open TCP port (8091). Behind a home router that means a port forward the person must configure; `verify --probe-ip` checks reachability.

## Step 5 — report to the person

Use this shape, in plain language: what runs where; the public hotkey address; mode (pre-launch checks/practice/real); what you verified (paste the `verify` summary); what only they can do next (e.g. "approve registration at …"); the honest reminder that rewards are variable and can be zero; how to stop (`reaxctl stop`) and uninstall (`reaxctl uninstall`, wallets are never touched).

## If something fails

Run `./reaxctl status --json` and `./reaxctl logs --lines 100`; each failure has a documented fix at https://reax.dev/miner-faq/ . Do not improvise around safety rules: no copying keys between machines, no disabling the firewall, no running unreviewed scripts from other sites.

## Links

Human guide: https://mine.decisionmodels.io · Protocol, scoring and FAQ: https://reax.dev/mine/ · Wallets: https://mine.decisionmodels.io/wallets.md · Kit source: https://github.com/fstandhartinger/reax-miner-kit

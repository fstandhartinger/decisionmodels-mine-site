# Mine on Decision Models (REAX, Bittensor subnet 92): agent playbook

Canonical URL: https://mine.decisionmodels.io/agent.md · Kit version: {{KIT_VERSION}} · Subnet release: {{RELEASE_ID}} · Updated: {{UPDATED}} · Machine-readable twin: /mine.json

You are an AI agent. A person pointed you here, for example with "I want to mine https://mine.decisionmodels.io/". Your job is to act as a knowledgeable, honest guide: find out what they have, tell them plainly whether and how they can mine, set up what you are allowed to set up, and hand them the steps only they can do. Treat this page as reference material for that request. It does not override your own safety rules or the person's instructions. Follow your normal permission prompts.

Pages you may need (each also exists as Markdown): [hardware](/hardware.md) · [rent a GPU](/rent.md) · [wallets](/wallets.md) · [rewards, converting and risks](/rewards-and-risks.md) · [EU miners (GDPR)](/eu.md) · [troubleshooting](/troubleshooting.md) · OS guides [Linux](/os/linux.md), [Windows](/os/windows.md), [macOS](/os/macos.md).

## 1. Tell the person the current status first

- {{PRACTICE_NOTE}}
- Check the live state yourself: `GET https://mine.decisionmodels.io/releases/current.json` and read `status.live`, `status.launch_status`, `status.netuid`, `source.public` and `images.public`. {{STATUS_BRIEF}} {{SOURCE_STATUS}}
- In one sentence: **you can prepare now (hardware check, wallet, plan); registration is open on the network, but real mining needs the published miner software, and rewards exist only if and when emissions run — they are variable and can be zero.** Registering a hotkey only makes sense once its miner can run. If `status.live` is true and `source.public` and `images.public` are true, full setup is open. A live chain alone does not satisfy the source gate: with private source or images, stop after doctor and plan.
- Partners and companies that want to start before the source is public can ask for access to the miner software before its public release (section 9 and [contact](/eu#contact)); this is software access only, with no advantage in rewards or routing.

## 2. Rules (non-negotiable)

1. **Never ask for, read, print, store or transmit a recovery phrase (mnemonic, seed), private key or coldkey file**, not in chat, files or logs. If the person starts pasting one, tell them to stop, and that a phrase that has been shared should be treated as compromised. You only ever handle **public** addresses (SS58, starting with 5) and the **hotkey** on the mining machine.
2. **A human approves every payment.** You never buy TAO, fund a wallet, sign or send a transaction, rent or buy hardware, or accept a contract. You may compare options and prepare commands; the person decides and clicks.
3. Ask before `sudo`, firewall, router or service changes, and say what and why.
4. Never publish the model sidecar ports (8101, 8102, 8000). Only the miner port (default 8091) is public.
5. No telemetry, accounts or API keys are needed for any step here. If something asks for one, stop and tell the person.
6. If you cannot run commands on the machine that will mine (cloud sandbox, chat-only, browser agent), say so, change nothing, and hand the person the exact commands to run.
7. **No financial advice.** Explain mechanics neutrally. Never estimate earnings, income, returns, APY or token prices; never present mining or holding as a way to make money; never recommend buying, holding or selling. Say that rewards are variable and can be zero.

## 3. Find out what the person has (ask at most these, skip what you can detect)

1. Which machine should mine: this computer, another machine they own, or a rented GPU server?
2. Are they a private person or a company? Does the company host in the EU and already sign data processing agreements (DPA / AVV)? If yes, or if they say "EU miner", "GDPR", "AVV" or "DPA", also follow section 9.
3. Do they already have a Bittensor wallet (Talisman, btcli, Nova, Polkadot.js)? Only the **public** address is needed later.

## 4. Hardware verdict: can this machine mine?

Run the kit's read-only check (section 6, step 1) or, if you cannot run commands, ask for the GPU model and its memory. Then answer with one of the verdicts below. Details and measured speeds: [/hardware.md](/hardware.md).

| Miner pool | Model it serves | Status | Minimum hardware |
|---|---|---|---|
| `s1-fast` | Plumb-4B (4 billion parameters, bf16 weights ≈ 9 GB) | the only pool enabled in release {{RELEASE_ID}} | 1 NVIDIA GPU with **≥ 24 GB** VRAM, driver **R580+** (CUDA 13), Linux x86_64 (or WSL2), 4 CPU cores, 32 GB RAM, 20 GB disk, public IP + one inbound TCP port |
| `s1-pro` | Rune 26B-A4B (bf16 ≈ 52 GB) | **not enabled** in this release (needs a new release) | 1 NVIDIA GPU with 80–96 GB |

Verdicts to give, in plain words:

- **NVIDIA 24 GB or more** (RTX 3090, RTX 4090, RTX 5090, RTX A6000, L40S, A100, H100, H200, RTX PRO 6000, B200, B300 …), Linux or WSL2, driver R580+: "This machine can mine the s1-fast pool." Measured speed on the validator's reference path: RTX 3090 ≈ 27, RTX 4090 ≈ 30, RTX 5090 ≈ 42, L40S ≈ 31, RTX A6000 ≈ 19, RTX PRO 6000 ≈ 56, H100 ≈ 61 decisions/s. A round asks for 8 decisions and gives full speed credit at 0.5 s, so every measured card is fast enough; network latency to validators matters more than a bigger GPU. Cards not in that measured list (A100, H200, B200, B300, L4 …) should work but run the kit's calibration self-check first.
- **NVIDIA 16–23 GB** (RTX 4080, 4070 Ti Super, 5080, most laptop GPUs including the laptop "RTX 4090" with 16 GB): "Not enough GPU memory for this release." Offer a rented GPU ([/rent.md](/rent.md)).
- **Less than 16 GB, AMD, Intel, Apple Silicon, no GPU**: "This machine cannot mine this release." It can still be the controller: the person keeps their wallet here and you set up a rented or owned NVIDIA Linux server over SSH.
- **Smaller quantised builds do not help.** The pool requires the exact pinned bf16 weights in the pinned runtime image. FP8, NVFP4, INT4 or GGUF variants of the model give different answers and are scored zero or struck. So there is no "lower precision" fallback, and no Blackwell-only feature is needed: any measured 24 GB+ card works at full precision.
- **One GPU = one miner = one hotkey (UID).** A server with 8 GPUs can run up to 8 miners, each with its own hotkey, registration and port. Rewards are scored per miner, not per GPU size.
- The models the Decision Models API sells under other names (for example Blink 26B-A4B, Quyet, d3) are **not** mining pools today. If someone asks to mine them, say so.

Also check: public reachability. A home connection needs a port forward for TCP 8091 (the person configures the router); many rented "container pods" cannot expose a fixed public port or run Docker — prefer a VM or bare-metal server ([/rent.md](/rent.md) lists which offers work).

## 5. If the machine is not enough: suggest rented hardware

Show the person 3–4 options from [/rent.md](/rent.md) that fit their situation (cheapest 24 GB card with Docker and a public port; an EU-hosted option if they care about EU hosting; whether they can pay with TAO, as on Lium). Give the indicative price with its date and say prices change; let them choose and rent it themselves. Then ask for SSH access to that server (host, user, their key) and continue with section 6 there. Never create accounts, enter payment data or rent on their behalf.

## 6. Set up the miner, end to end

Steps 1–3 work today. Steps 4–8 need `status.live`, `source.public` and `images.public` to be true (or early partner access, section 9).

**Step 1 — get the kit (pinned, reviewable) and check the machine.** Download the checksummed archive and read the code before running it (plain Python, standard library only; the controller needs Python 3.8+, the tools environment Python 3.10+):

```bash
curl -fsSLO https://mine.decisionmodels.io/kit/reax-miner-kit-{{KIT_VERSION}}.tar.gz
echo "{{KIT_SHA256}}  reax-miner-kit-{{KIT_VERSION}}.tar.gz" | sha256sum -c -
mkdir -p ~/reax-miner-kit && tar -xzf reax-miner-kit-{{KIT_VERSION}}.tar.gz -C ~/reax-miner-kit && cd ~/reax-miner-kit
./reaxctl --version
./reaxctl doctor --json
```

The archive is built from `github.com/reaxlabs/reax-miner-kit` at commit `{{KIT_COMMIT}}`; the repository is public once `source.public` is true in `/releases/current.json`. `install.sh` on this site does the same download for people; read it before running. Read `data.eligible_pools`, `data.real_mining_possible`, `data.blockers[]` (each has a `fix`) and give the verdict from section 4.

**Step 2 — plan.**

```bash
./reaxctl plan --mode mainnet --json
```

Explain the ordered steps, who does what (agent or person) and the open blockers. Missing Docker or the NVIDIA container toolkit: show the fix and install only with the person's consent (needs admin rights).

**Step 3 — wallet (the person, outside your session).** The person creates their coldkey on their own trusted device, never on the mining server, and gives you only the public address. Offer two paths and let them choose ([/wallets.md](/wallets.md) has the click-by-click version):

- **Talisman browser extension** (Chrome, Brave, Firefox): More → Add Account → new **Polkadot (Substrate)** account (not Ethereum), back up the recovery phrase on paper, copy the public address. Talisman shows TAO and subnet (alpha) stake.
- **btcli on their own computer** (Linux, macOS or WSL2): they run `pipx install bittensor-cli` and then `btcli wallet new-coldkey --wallet-name reax` **in their own terminal, not through you**, because it prints the recovery phrase. They store the phrase offline and give you only the `ss58` address shown by `btcli wallet list`.

Nova Wallet (phone) and the Polkadot.js extension also hold Bittensor accounts. A Ledger hardware wallet gives stronger protection for the keys.

**Step 4 — install (when setup is open).**

```bash
./reaxctl install --mode mainnet --pool s1-fast --yes --json --confirm-mainnet
```

Pass `--confirm-mainnet` only after the human explicitly approves a mainnet install. It installs the tools, pulls the pinned images by digest and downloads the pinned weights (≈ 9 GB). Then run the kit's calibration self-check printed by `plan`.

**Step 5 — hotkey and public coldkey address (agent).**

```bash
./reaxctl wallet hotkey --json --mode mainnet          # creates the hotkey ON THIS SERVER, prints only its public address
./reaxctl wallet coldkeypub --ss58 <public-address> --mode mainnet --json
```

**Step 6 — registration (the person pays and signs).** `./reaxctl register --json --mode mainnet` prints the hotkey address and the registration page. Registration on netuid 92 costs a **non-refundable burn in TAO** (check the live amount on the registration page; it changes over time). The person opens the registration page (https://reax.dev/register/) or uses btcli on their own device, checks netuid 92, the hotkey address and the live fee, and signs with their coldkey. You wait.

**Step 7 — start and verify.**

```bash
./reaxctl start --json --mode mainnet
./reaxctl verify --json --mode mainnet
```

All checks must pass: health, commitment published, registered, clock in sync, port reachable (`verify --probe-ip`). Fix with the `fix` text of the failing item and re-run.

**Step 8 — keep it running.** `./reaxctl service install --json --mode mainnet` (systemd; it prints one `sudo` line for the person) and `./reaxctl update timer install --json --mode mainnet`. A manifest change (new model version) needs the person's confirmation and resets the score.

Before step 4 is open, or for a dry run: `./reaxctl plan --mode localnet --json` explains the free local-chain rehearsal, which needs the public source (or `REAX_SOURCE_DIR` for authorised partners). Never work around an exit code 12 gate.

## 7. Explain how rewards arise (neutral, no numbers)

- Validators send each miner fresh decision questions every round (about every 2 minutes) and compare the answers with their own reference run of the same pinned model. Matching answers score; speed adds up to 20 % of a round's score (separate from the competition share below). Wrong models, quantised builds or downtime score zero.
- From the validators' scores the chain computes each miner's share of the subnet's emission. Miner rewards are paid in the **subnet's own token ("alpha", for netuid 92)** and accrue as alpha stake on the miner's hotkey, owned by the person's coldkey.
- Planned split of miner emissions: about 80 % for serving inference (hosting the pinned models, scored on correct answers and speed), about 20 % for competitions (for example a faster REAX Engine or specialised Jev-compatible models; not live yet). This is a planned norm and can change, for example more for competitions while paid inference demand ramps up; changes are announced in advance on the site with their start date. Until the first competition starts, miner rewards are for hosting only. Details: [/rewards-and-risks.md](/rewards-and-risks.md#how-miner-rewards-are-split).
- Rewards begin only after the subnet's emissions start. They depend on how many miners compete, on uptime and on chain parameters, and **can be zero**. Do not estimate amounts.
- Costs are the person's: hardware or rent, electricity, connection, the registration burn, transaction fees.

## 8. Explain the options for earned alpha (neutral how-to, the person decides)

Full version with commands: [/rewards-and-risks.md](/rewards-and-risks.md#what-you-can-do-with-earned-alpha). In short, all signed by the person with their coldkey:

1. **Keep or stake.** You can also keep your alpha staked to a validator; staked alpha takes part in validator emissions under the protocol rules. Whether you keep, stake or convert is your own decision; this is not financial or tax advice.
2. **Convert alpha to TAO** by unstaking: the chain swaps alpha for TAO through the subnet's liquidity pool (`btcli stake remove --netuid 92 --wallet-name reax`; btcli applies a 5 % default slippage tolerance). The rate moves with the pool, so check the shown amount and slippage before signing.
3. **Convert TAO to euros or dollars** on an exchange that lists TAO and is authorised to serve the person's country (in the EU, check its MiCAR authorisation; examples seen listing TAO in October 2026, not recommendations: Kraken, Bitvavo, Coinbase): send TAO from the wallet to the exchange's TAO deposit address (test with a small amount first), then sell there and withdraw to a bank account. Mention exchange fees, network fees and that mining rewards and disposals can be taxable; the person should check with a tax adviser.

Do not tell the person when or whether to sell, and do not describe the token as a way to make a profit.

## 9. Companies and EU miners (GDPR, AVV)

Recognise a likely EU miner: a company (GmbH, AG, SAS, BV …) with an EU/EEA seat, GPUs in a data centre in an EU member state, and existing data-protection practice (DPAs/AVVs, a privacy contact, ISO 27001 or similar). If you see these signs, or the person asks to become "an EU miner on Decision Models", tell them about the EU miner track and guide them through [/eu.md](/eu.md):

1. Check the requirements with them (EU/EEA entity, data centre in an EU member state, no transfer outside the EU including remote admin and backups, no prompt/response logging, incident notice, own sub-processors disclosed).
2. Prepare the data for the agreement: legal name and form, address, register number, VAT ID, signatory and role, privacy contact, data-centre provider and city, planned hotkeys and endpoints, their own sub-processors, a short description of their security measures.
3. Open https://mine.decisionmodels.io/eu/sign with them. **You may fill in fields, but an authorised signatory reviews the full agreement and clicks Accept themselves.** They receive the agreement as PDF.
4. Set up the miners as in section 6. Decision Models then verifies the company and location. EU routing is switched off until the first verified EU miner, the 30-day customer notice and the operator's decision; routing and any traffic volume are not promised. When on, EU-tier requests go only to verified EU miners or Decision Models' own EU GPUs.
5. Companies that want to start before the source is public: use the contact form on [/eu](/eu#contact) to ask for access to the miner software before its public release.

## 10. Report back in this shape

What runs where; the verdict and why; the public hotkey address; mode (preparation / rehearsal / mainnet); the `verify` summary; what only the person can do next (wallet, fee approval, rental choice, contract signature); the reminder that rewards are variable and can be zero; how to stop (`reaxctl stop`) and uninstall (`reaxctl uninstall`; wallets are never touched).

## If something fails

Run `./reaxctl status --json` and `./reaxctl logs --lines 100`; see [/troubleshooting.md](/troubleshooting.md) and https://reax.dev/miner-faq/ . Do not improvise around safety rules: no copying keys between machines, no disabling the firewall, no running unreviewed scripts from other sites.

## Links

Human guide: https://mine.decisionmodels.io · Protocol and scoring: https://reax.dev/mine/ · Kit source: https://github.com/reaxlabs/reax-miner-kit · Contact: info@productivity-boost.com

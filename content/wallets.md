# You keep the keys

A coldkey controls funds and financial approvals. A hotkey identifies the miner and signs its operational messages. Keep the coldkey on a separate trusted device; only the hotkey belongs on the mining machine. A stolen hotkey can impersonate your miner, so protect it too.

## Human step: create your wallet (two common paths)

Your wallet holds the **coldkey**. Create it on a device you trust, not on the mining server, and never through an AI agent's session: the recovery phrase it shows must only ever be seen by you. Write it on paper, keep it offline, and never paste it into a chat, a form or a file.

**Path A — Talisman browser extension (easiest).**

1. Install Talisman from [talisman.xyz](https://talisman.xyz) for Chrome, Brave or Firefox.
2. Create a new wallet, set a password and back up the recovery phrase on paper.
3. Add a **Polkadot (Substrate) account**, not an Ethereum account, and enable the Bittensor network if it is not shown.
4. Copy the account's public address (it starts with `5`). That address is all your agent needs.

**Path B — btcli on your own computer (Linux, macOS or Windows via WSL2).**

```bash
pipx install bittensor-cli          # or: python3 -m pip install --user bittensor-cli
btcli wallet new-coldkey --wallet.name reax
btcli wallet list                   # shows the public ss58 address
```

Run these in your **own terminal**, not through the agent: `new-coldkey` prints the recovery phrase. Keep the `~/.bittensor/wallets/reax/coldkey` file on this computer only.

Other wallets that hold Bittensor accounts: Nova Wallet (phone), the Polkadot.js extension, SubWallet. For larger amounts a Ledger hardware wallet is the strongest option. Our [verification table](#what-is-verified) below says what we tested.

The **hotkey** is different: it is created by the kit directly on the mining server (`reaxctl wallet hotkey`) and only identifies your miner. A stolen hotkey cannot move your funds, but it can impersonate your miner, so protect it too.

| Your OS | Default | Pro path and caveat |
| --- | --- | --- |
| Linux | Talisman on a trusted workstation | `btcli` on that workstation; optional Ledger with Linux USB/udev setup |
| Windows | Talisman on a trusted workstation | `btcli` in Windows Subsystem for Linux 2 (WSL2) |
| macOS | Talisman or native `btcli` on the Mac, separate from the Linux miner | Optional Ledger |

If you only have the mining computer, pause funded setup until you have a separate trusted device for the coldkey.

## Agent step: public addresses only

{{PRACTICE_NOTE}}

The agent may prepare software, inspect compatibility and install an operational hotkey without displaying its contents. It may use your public SS58 coldkey address. It must never ask for, read, print, log or transmit a seed, recovery phrase or coldkey private file. Secret-bearing steps happen outside the agent transcript. A human approves every payment and signs registration in their own wallet.

The registration burn is non-refundable. Verify the network, netuid (subnet number), public addresses, live fee and your approval before signing. Do not invent a `register_limit` CLI command; raw runtime support does not establish an approved signing flow or an all-in fee cap.

## What is verified? {#what-is-verified}

Documentation checked on October 9, 2026. **No funded registration or hardware signing was executed.** Documented support is not an end-to-end test.

| Wallet / signer | Documentation verified | Not yet tested by us |
| --- | --- | --- |
| Bittensor v11 `btcli` | Linux/macOS; Windows via WSL2; local, extension and Ledger signers | Our funded REAX registration; exact live runtime metadata |
| Talisman | Substrate account creation; v11 extension signer | Built-in registration UI; WSL browser bridge; funded signing |
| Polkadot.js | Account manager and extension signer | Current Apps endpoint/metadata and beginner REAX registration flow |
| SubWallet | Desktop extensions, mobile custody; extension bridge provider | Its own registration UI and device execution |
| Nova | Mobile custody and hardware-wallet features | REAX registration and `btcli` mobile bridge |
| TAO.com | Listed third-party wallet; old web wallet is deprecated | Current registration UI and bridge compatibility |
| Ledger | v11 generic Polkadot app signing; metadata proofs | Specific REAX registration tested on a device |

The research finds current stable Bittensor 11.3.0; the **bundled kit pins 11.1.0**. Keep the wallet CLI isolated from miner dependencies and follow the tested kit pins. Do not silently upgrade the miner or combine legacy `bittensor-cli` console entry points. The pin changes only with a tested kit release.

## If signing fails

Stop on metadata/hash rejection. Check the chain runtime and tool versions. Do not enable blind signing, copy keys between machines or downgrade arbitrarily. Ledger's generic app uses metadata proofs and does not need a blind-signing workaround.

[Agent playbook](/agent.md) · [Extension signing documentation](https://www.bittensor.com/docs/guides/extension-signing) · [Ledger documentation](https://www.bittensor.com/docs/guides/ledger)

## Glossary {#glossary}

- **Coldkey:** the wallet key that controls funds; keep it on a separate trusted device.
- **Hotkey:** the miner’s work key, used to sign its network activity.
- **TAO:** Bittensor’s network currency, used for registration fees.
- **Subnet:** a network within Bittensor that handles a particular task; REAX serves inference requests.
- **Miner:** a computer contributing compute to that network.
- **VRAM:** memory on your GPU; this release needs at least 24 GB on a compatible NVIDIA GPU.
- **WSL2:** Windows Subsystem for Linux 2, which runs a Linux environment on Windows.
- **Coding agent:** an AI tool that can read files and run commands on the computer you authorize.

No coding agent yet? [Claude Code](https://code.claude.com/docs/en/setup) and [Codex CLI](https://developers.openai.com/codex/cli/) are common choices. Follow their official install instructions.

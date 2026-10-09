# You keep the keys

A coldkey controls funds and financial approvals. A hotkey identifies the miner and signs its operational messages. Keep the coldkey on a separate trusted device; only the hotkey belongs on the mining machine. A stolen hotkey can impersonate your miner, so protect it too.

## Human step: choose your signer

Our recommended default is **Talisman on a separate trusted workstation**, using a Substrate/Polkadot account. Use [REAX's wallet walkthrough](https://reax.dev/wallet/) for screenshots and [the registration tool](https://reax.dev/register/) when launch permits it. An EVM account is not the right account type.

| Your OS | Default | Pro path and caveat |
| --- | --- | --- |
| Linux | Separate trusted Talisman workstation | Isolated `btcli` environment; optional Ledger with Linux USB/udev setup |
| Windows | Separate trusted Talisman workstation | `btcli` in Windows Subsystem for Linux 2 (WSL2); Windows browser bridge is not yet tested by us end to end. Use a separate Linux/macOS signer if it fails |
| macOS | Talisman on the controller, separate from the Linux miner | Native `btcli`; optional Ledger |

Windows host and WSL are one machine for custody. If you only have the mining computer, pause funded setup until you have a separate trusted signer. A phone wallet alone is not a verified REAX registration solution.

## Agent step: public addresses only

{{PRACTICE_NOTE}}

The agent may prepare software, inspect compatibility and install an operational hotkey without displaying its contents. It may use your public SS58 coldkey address. It must never ask for, read, print, log or transmit a seed, recovery phrase or coldkey private file. Secret-bearing steps happen outside the agent transcript. A human approves every payment and signs registration in their own wallet.

The registration burn is non-refundable. Verify the network, netuid (subnet number), public addresses, live fee and your approval before signing. Do not invent a `register_limit` CLI command; raw runtime support does not establish an approved signing flow or an all-in fee cap.

## What is verified?

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

The research finds current stable Bittensor 11.3.0; the **bundled kit pins 11.1.0**. Keep the wallet CLI isolated from miner dependencies and follow the tested kit pins. Do not silently upgrade the miner or combine legacy `bittensor-cli` console entry points. This version difference needs release-owner review.

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

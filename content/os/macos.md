# macOS: check your host, plan a controller and signer

A Mac cannot mine this release locally. The runtime requires NVIDIA CUDA 13 on a Linux x86_64 host. Apple GPUs and Docker architecture emulation cannot supply that hardware. {{HUMAN_NOTE}}

## Agent step: check and plan here

Follow the [agent playbook](/agent.md).

```bash
./reaxctl doctor --json
./reaxctl plan --mode localnet --json
```

## Human step: authorize a remote host

A Mac can control an existing NVIDIA Linux machine over SSH. Tell the agent exactly which host you authorize. The agent must identify where every command runs, then inspect that host before installing anything. A hosted coding-agent sandbox is not automatically your GPU server.

Do not rent hardware or approve a paid service through an agent without a specific human decision. The remote host needs at least 24 GB NVIDIA VRAM (GPU memory) for s1-fast, R580+, 4 CPU cores, 32 GB RAM, 20 GB disk and public TCP 8091. Keep the model’s supporting services (sidecars) private.

## Human step: keep the coldkey (funds key) separate

Talisman on a trusted Mac can be the coldkey signer for a separate Linux miner. Native macOS `btcli` is the pro path; optional Ledger signing is documented. No funded signing flow was executed in our research. Never put the coldkey seed or private file on the remote host, in chat or in logs.

[Linux host guide](/os/linux) · [Wallet guide](/wallets) · [REAX FAQ](https://reax.dev/miner-faq/)

[Mining terms explained](/wallets#glossary)

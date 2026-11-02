# Linux: the native mining host

Linux x86_64 with a compatible NVIDIA GPU is the default path for this release. {{HUMAN_NOTE}}

## Agent step: inspect before changing anything

Run the pinned kit's read-only check:

```bash
./reaxctl doctor --json
./reaxctl plan --mode localnet --json
```

The current validator pool rules have four pools. For s1-fast, one NVIDIA GPU with 24 GB or more VRAM (GPU memory), an R580+ driver for CUDA 13, 4 CPU cores, 32 GB RAM and 20 GB free disk are required. The active s1-pro pool uses mammoth-1 (manifest 3f3558e583b0a1d6), effective since 30 October 2026 at 09:00 UTC; it needs an NVIDIA GPU with at least 48 GB and about 80 GB of disk. Only the RTX PRO 6000 Blackwell Server Edition has been measured; other cards must pass the self-check. s1-lite needs an NVIDIA GPU with 8 GB or more (Jetson Orin 8 to 64 GB is not yet calibrated on real hardware), and s1-cpu works on any x86-64 CPU with AVX2 or ARMv8.2 CPU with 4 or more cores and 4 GB RAM (no GPU). The bundled kit 0.1.8 and release descriptor post7 still pin Rune for s1-pro; follow the [hardware guidance](/hardware) and require a passing mammoth self-check before committing. Docker Engine, Compose and the NVIDIA Container Toolkit must work together. A reported CUDA version alone does not prove the pinned model runs. Other NVIDIA cards need calibration; see the [release descriptor](/releases/current.json).

## Agent step: practice first

Follow the [agent playbook](/agent.md).

## Human step: permissions and custody

Approve admin changes before Docker/toolkit installation. Keep the funded coldkey (funds key) on a separate trusted device. The miner gets only the operational hotkey (miner’s work key) and public coldkey address. See [wallet guidance](/wallets).

## Networking

A public IP and inbound TCP 8091 are required. Approve any router/firewall changes. Never expose the model’s supporting services (sidecars) on ports 8101, 8102 or 8000. Carrier-grade NAT may prevent inbound connections; do not assume port forwarding fixes it. Check actual external reachability before a payment.

## AMD or no GPU

This release does not support AMD GPUs, but a machine without a supported NVIDIA GPU can still serve the s1-cpu pool (x86-64 with AVX2, or ARMv8.2, 4 or more cores); see [hardware](/hardware). {{GPU_NOTE}} A separately owned or approved remote NVIDIA Linux host is another route; the agent must never rent it itself.

[Protocol and scoring](https://reax.dev/mine/) · [Troubleshooting](/troubleshooting)

[Mining terms explained](/wallets#glossary)

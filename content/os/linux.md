# Linux: the native mining host

Linux x86_64 with a compatible NVIDIA GPU is the default path for this release. {{HUMAN_NOTE}}

## Agent step: inspect before changing anything

Run the pinned kit's read-only check:

```bash
./reaxctl doctor --json
./reaxctl plan --mode localnet --json
```

Release 1.2.0rc11.post7 has four pools. For s1-fast, the bundled release requires one NVIDIA GPU with 24 GB or more VRAM (GPU memory), R580+ driver for CUDA 13, 4 CPU cores, 32 GB RAM and 20 GB free disk; s1-pro needs 80 to 96 GB and about 80 GB of disk, s1-lite an NVIDIA GPU with 8 GB or more (Jetson Orin 8 to 64 GB is not yet calibrated on real hardware), and s1-cpu any x86-64 CPU with AVX2 or an ARMv8.2 CPU with 4 or more cores and 4 GB RAM (no GPU). See [hardware](/hardware) for each pool. Docker Engine, Compose and the NVIDIA Container Toolkit must work together. A reported CUDA version alone does not prove the pinned model runs. Other NVIDIA cards need calibration; see the [release descriptor](/releases/current.json).

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

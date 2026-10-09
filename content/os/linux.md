# Linux: the native mining host

Linux x86_64 with a compatible NVIDIA GPU is the default path for this release. {{PRACTICE_NOTE}}

## Agent step: inspect before changing anything

Run the pinned kit's read-only check:

```bash
./reaxctl doctor --json
./reaxctl plan --mode localnet --json
```

For s1-fast, the bundled release requires one NVIDIA GPU with at least 24 GB VRAM, R580+ driver for CUDA 13, 4 CPU cores, 32 GB RAM and 20 GB free disk. Docker Engine, Compose and the NVIDIA Container Toolkit must work together. A reported CUDA version alone does not prove the pinned model runs. Other NVIDIA cards need calibration; see the [release descriptor](/releases/current.json).

## Agent step: practice when source is public

Follow the [agent playbook](/agent.md). {{PRACTICE_NOTE}}

## Human step: permissions and custody

Approve admin changes before Docker/toolkit installation. Keep the funded coldkey on a separate trusted device. The miner gets only the operational hotkey and public coldkey address. See [wallet guidance](/wallets).

## Networking at launch

A public IP and inbound TCP 8091 are required. Approve any router/firewall changes. Never expose sidecar ports 8101, 8102 or 8000. Carrier-grade NAT may prevent inbound connections; do not assume port forwarding fixes it. Check actual external reachability before a payment.

## AMD or no GPU

This CUDA release does not support AMD GPUs or CPU mining. {{GPU_NOTE}} A separately owned or approved remote NVIDIA Linux host is another route; the agent must never rent it itself.

[Protocol and scoring](https://reax.dev/mine/) · [Troubleshooting](/troubleshooting)

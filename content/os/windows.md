# Windows: a conditional WSL2 path

Native Windows mining is unsupported. NVIDIA CUDA containers can run through WSL2, but the complete REAX Windows path is **not yet tested by us**. Generic CUDA support is not proof that this miner works. {{PRACTICE_NOTE}}

## Human step: choose the host

Prefer Windows 11 with a supported NVIDIA GPU and a current Windows production driver, R580+ for the pinned CUDA 13 runtime. Older GPU families may lack CUDA 13 library support. Windows 10 Home/Pro standard support ended on October 14, 2025; any extended support is specific to your device.

Windows and its WSL VM count as the same machine for custody. A funded browser coldkey on the Windows mining host is not a separate signer.

## Agent step: inspect WSL2

Update WSL2 with approval and use a supported Linux distribution. Docker Desktop must use its WSL2 backend with distribution integration. Do not install a Linux NVIDIA display driver inside WSL: the Windows driver provides the CUDA interface.

```bash
nvidia-smi
./reaxctl doctor --json
./reaxctl plan --mode localnet --json
```

If `nvidia-smi` is not on PATH, NVIDIA documents `/usr/lib/wsl/lib/nvidia-smi`. Actual pinned-container and model health checks remain necessary. WSL has limited GPU observability.

## Networking needs a real check

Docker Desktop networking and Docker Engine inside WSL differ. Desktop host networking is an opt-in feature in version 4.34+, not the same as a native Linux host. WSL NAT, Windows firewall and home-router forwarding can each block inbound TCP. Windows 11 mirrored networking is conditional on supported versions; do not promise it fixes public ingress. Check reachability again after a reboot.

Only TCP 8091 may be public. Ports 8101, 8102 and 8000 stay private. Ask before changing permissions or networking.

## Human step: wallet signing

Recommended default: Talisman on a separate trusted workstation. `btcli` runs in WSL2, but the WSL2-to-Windows-browser extension bridge is **not yet tested by us** end to end. If it fails, use a supported separate Linux/macOS signer. Never export the seed to solve a bridge problem. Ledger over WSL USB attachment is documented, not device-tested here.

## Start with checks; practice once source is public

{{PRACTICE_NOTE}} The [playbook](/agent.md) explains the practice flow once source is public. NVIDIA below 24 GB, AMD and no-GPU machines cannot mine this release.

[Wallet guide](/wallets) · [NVIDIA WSL guidance](https://docs.nvidia.com/cuda/wsl-user-guide/index.html) · [Docker GPU guidance](https://docs.docker.com/desktop/features/gpu/)

# Hardware: which machines can mine

{{HUMAN_NOTE}}

A REAX miner serves one pinned model exactly as the validators run it. Validators compare every answer with their own reference run, so the hardware has to run the **exact pinned weights at full (bf16) precision in the pinned runtime image**. That makes the check simple: enough NVIDIA GPU memory, a recent driver, Linux, and a reachable port.

## Miner pools in release {{RELEASE_ID}}

| Pool | Model | Status | GPU | Rest of the machine |
|---|---|---|---|---|
| `s1-fast` | Plumb-4B, 4 B parameters, bf16 weights ≈ 9 GB | **enabled**, the only pool at launch | 1 NVIDIA GPU, **≥ 24 GB** VRAM, driver R580+ (CUDA 13) | Linux x86_64 (WSL2 conditional), 4 CPU cores, 32 GB RAM, 20 GB free disk, Docker + NVIDIA container toolkit, public IP with inbound TCP 8091, synchronised clock |
| `s1-pro` | Rune 26B-A4B, bf16 ≈ 52 GB | **not enabled** in this release; switching it on needs a new release | 1 NVIDIA GPU, 80–96 GB | 80 GB free disk |

Is the fast model easy to run at home? **Yes, if you have a 24 GB NVIDIA card** such as an RTX 3090, 4090 or 5090. It is a small 4-billion-parameter model. It does not fit on cards with 16 GB or less, and it does not run on Apple, AMD or Intel GPUs, because the runtime is a pinned CUDA build.

## Measured cards (s1-fast)

Decisions per second on the validator's reference path, one decision at a time (from the subnet's calibration, October 2026). A round asks for 8 decisions and gives full speed credit at 0.5 s, so every card below is fast enough; latency between you and the validators matters more than a faster GPU.

| Card | VRAM | Decisions/s | Verdict |
|---|---|---|---|
| RTX 3090 | 24 GB | ≈ 27 | eligible |
| RTX 4090 | 24 GB | ≈ 30 | eligible |
| RTX 5090 | 32 GB | ≈ 42 | eligible |
| RTX A6000 | 48 GB | ≈ 19 | eligible |
| L40S | 48 GB | ≈ 31 | eligible |
| RTX PRO 6000 Blackwell | 96 GB | ≈ 56 | eligible |
| H100 80GB | 80 GB | ≈ 61 | eligible |
| A100, H200, B200, B300, A10/L4 (24 GB) | ≥ 24 GB | not yet measured | should work; run the kit's calibration self-check before serving |
| RTX 4080/5080, 4070 Ti Super, laptop GPUs (incl. laptop "RTX 4090", 16 GB) | 16 GB | — | not enough memory |
| Apple Silicon, AMD, Intel, no GPU | — | — | cannot mine; can act as the controller for a remote NVIDIA server |

Two machines with the same card can still give slightly different results, so the kit runs a self-check on your machine before you start serving.

## No lower-precision fallback

Quantised versions of the model (FP8, NVFP4, INT4, GGUF) answer slightly differently. The validators detect that and score those miners zero or strike them. So there is no reduced-precision mode for smaller cards, and nothing in this release needs Blackwell-only formats: any card in the table above runs the model in bf16.

## Several GPUs, big nodes

One GPU runs one miner, and each miner has its own hotkey, registration (UID) and port. Rewards are scored per miner; a larger GPU does not receive a larger share per miner. A server with several GPUs (for example H100/H200/B200/B300 ×8) runs one s1-fast miner per GPU: one `--home` per GPU, each with `--gpu N`, its own `--miner-port` and `--hotkey-name`, and one shared weights copy via `--weights-dir`:

```bash
reaxctl install --home ~/.reax-miner-gpu1 --gpu 1 --miner-port 8092 --hotkey-name miner2 \
  --weights-dir /srv/reax-weights --mode mainnet --confirm-mainnet
```

Example, 8x B300: 8 miners, 8 hotkeys (each registered separately), ports 8091 to 8098, GPUs 0 to 7, one weights copy. Give each miner its own GPU and its own public port; do not share a GPU with other work. One hotkey spread over many GPUs is planned but not active, and no extra reward exists for it today. For what runs on such a node and which rights it needs, see [Security](/security). No pool beyond s1-fast is enabled in this release.

## Network

The miner needs a public IPv4 or IPv6 address with one inbound TCP port (default 8091). At home that means a port forward on your router. If a provider maps another external port, set `REAX_EXTERNAL_PORT` to it. Many rented "container pods" cannot run Docker or expose a fixed port; choose a VM or bare-metal server. See [rent a GPU](/rent).

## How your agent checks this

```bash
./reaxctl doctor --json
```

It reports the GPU, VRAM, driver, Docker, NVIDIA toolkit, disk, RAM, clock and ports, lists `eligible_pools` and gives a `fix` for every blocker. [Agent playbook](/agent.md) · [Rent a GPU](/rent) · [Troubleshooting](/troubleshooting)

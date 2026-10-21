# Hardware: which machines can mine

{{HUMAN_NOTE}}

A REAX miner serves one pinned model exactly as the validators run it. Validators compare answers with their own reference run, so the machine has to run the **exact pinned weights in the pinned runtime image**. Release {{RELEASE_ID}} has four pools, from an 80 GB datacenter GPU down to a plain CPU. One hotkey serves one pool and commits to it as `reax-s1/1:<pool>:<manifest_id>`; the miner CLI does this for you. From block 9331987 (about 13:00 UTC on 21 October 2026) one hotkey can serve several pools, see [below](#several-models-and-a-competition-entry-on-one-hotkey-from-block-9331987).

## Miner pools in release {{RELEASE_ID}}

| Pool | Model | Hardware | Share of the inference part |
|---|---|---|---|
| `s1-fast` | Plumb-4B, bf16 weights ≈ 9 GB | NVIDIA GPU, **≥ 24 GB** VRAM, driver R580+ (CUDA 13) | GPU tier 80 %, 35 % of it |
| `s1-pro` | Rune 26B-A4B v3, bf16 ≈ 52 GB (gated on Hugging Face) | NVIDIA GPU, **80–96 GB** VRAM | GPU tier 80 %, 65 % of it |
| `s1-lite` | Plumb-4B, 8-bit GGUF (4.48 GB), llama.cpp | NVIDIA GPU with **≥ 8 GB**, including Jetson Orin (8 GB or more) | small-GPU tier 15 % |
| `s1-cpu` | Gutsy 0.8B, 8-bit GGUF (0.81 GB), llama.cpp | any x86-64 CPU with AVX2 or an ARMv8.2 CPU, 4+ cores, 4 GB RAM | CPU tier 5 % |

Shares apply to the inference part of miner emissions (all of it before the competitions start, 50 % after; see [rewards](/rewards-and-risks#how-miner-rewards-are-split)). Two rules shape them:

- **Tier order:** the average per miner in a tier is at most half of the tier above.
- **Empty pools:** if a pool has no miner, its share passes to the other pools. Nothing is burned.

Tiers, shares and targets are release constants. A change needs a new release and is announced in advance.

Common to the GPU pools: Linux x86_64 (WSL2 conditional), 4 CPU cores, 32 GB RAM, Docker + NVIDIA container toolkit, public IP with inbound TCP 8091, synchronised clock. Free disk per pool: `s1-fast` 20 GB, `s1-pro` 80 GB, `s1-lite` 8 GB, `s1-cpu` 3 GB.

Is the fast model easy to run at home? **Yes, if you have a 24 GB NVIDIA card** such as an RTX 3090, 4090 or 5090. With a smaller NVIDIA card (8 GB or more) or no GPU, use `s1-lite` or `s1-cpu`. Apple, AMD and Intel GPUs are not used; the GPU runtimes are pinned CUDA builds.

Since 1.2.0rc3 your pay inside a pool follows the throughput the validator verifies; set `REAX_PER_CALLER_CONCURRENCY=32` and `REAX_PER_CALLER_PER_MINUTE=456` (the defaults of the 1.2.0rc10.post1 miner image) so a probe can measure your full speed.

## s1-pro: Rune 26B-A4B v3 (80–96 GB)

| GPU | VRAM | Status |
|---|---|---|
| RTX PRO 6000 Blackwell | 96 GB | measured, bit-identical to the reference |
| H100 | 80 GB | measured, bit-identical to the reference |
| H200, B200 | | expected to work, not measured |
| A100 | 80 GB | not measured; at your own risk, run the self-check first |
| Cards below the 80 GB class | | cannot hold the 52 GB weights plus KV cache |

- **Deterministic runtime, required.** Use `runtimes/s1-pro` with `RUNE_DETERMINISTIC=1` (the default). Other builds are not accepted: stock vLLM gives different numbers under different load and scores only about 65 % of its rounds; FP8 or online-quantised builds score about 12 % of rounds and are struck in about 22 % of them.
- **Gated weights.** The Hugging Face repo `surogate/rune-26b-a4b-GGUF` (bf16 safetensors despite the name) is gated. Accept the gate with your own Hugging Face account and run `hf auth login`. REAX never mirrors the weights, and `reaxctl` never asks for your token.
- **Confidential-compute cloud GPUs:** the runtime container needs `-v "$(pwd)/runtimes/vllm-ccfix:/opt/reax-ccfix:ro" -e PYTHONPATH=/opt/reax-ccfix -e REAX_VLLM_DISABLE_UVA=1`; without it vLLM returns garbage there. Results are unchanged.
- **Kit command:** `./reaxctl install --mode mainnet --pool s1-pro --yes --json --confirm-mainnet`, then the self-check `reax-selfcheck --model s1-pro`. It must print PASS before you commit.
- Each round asks 8 decisions and verifies 3; a round in tolerance scores `0.8 + 0.2 × speed` (full speed at 1 s, zero at 12 s). Capacity target: 10 decisions per second.

## s1-lite: small GPU, including Jetson Orin

- **Model:** the s1-fast model Plumb-4B v5 as `GGUF Q8_0` (4.48 GB, pinned file) on llama.cpp CUDA (`runtimes/s1-gguf`). Same prompt and temperature as s1-fast.
- **Hardware:** NVIDIA GPU with 8 GB or more. A Jetson Orin (JetPack 6) with 8 GB or more unified memory uses the arm64 Jetson image. The Orin Nano 4 GB is too small. Small-GPU and Jetson hardware is **not yet calibrated on real hardware**.
- **One file per pool:** a Q4 file does not pass (mean logit distance 0.60 against 0.11 for Q8); use the pinned Q8_0 file.
- **Scoring:** 4 items per round, all verified; latency full at 1 s, zero at 12 s. Capacity target 8 decisions per second. A desktop GPU fills it; an Orin reaches a fraction. Measured in the sidecar: RTX 5070 Ti 33 decisions/s, RTX A6000 24/s.
- **Kit command:** `./reaxctl install --mode mainnet --pool s1-lite --yes --json --confirm-mainnet`

## s1-cpu: no GPU needed

- **Model:** Gutsy 0.8B v0.4 (Apache-2.0) as `GGUF Q8_0` (812 MB) on llama.cpp CPU.
- **Hardware:** any x86-64 CPU with AVX2 or an ARMv8.2 CPU, 4+ cores, 4 GB RAM.
- **Speed:** about 1 s per decision on 4 cores, 0.7–1.0 s on 8 cores.
- **Scoring:** 4 items per round, all verified; latency full at 2 s, zero at 30 s. Capacity target 1 decision per second. Answers on x86 and ARM match within a small margin (mean logit distance 0.035 on ARM, emulated).
- **Kit command:** `./reaxctl install --mode mainnet --pool s1-cpu --yes --json --confirm-mainnet`

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
| RTX 4080/5080, 4070 Ti Super, laptop GPUs (incl. laptop "RTX 4090", 16 GB) | 16 GB | — | not enough memory for s1-fast; can serve `s1-lite` |
| Apple Silicon, AMD, Intel, no GPU | — | — | no GPU pool; a CPU can serve `s1-cpu`; can also act as the controller for a remote NVIDIA server |

Two machines with the same card can still give slightly different results, so the kit runs a self-check on your machine before you start serving.

## One file per pool, no other precision

Each pool has exactly one pinned build. `s1-fast` and `s1-pro` require the bf16 weights in the pinned runtime; `s1-lite` and `s1-cpu` require the pinned 8-bit GGUF file. A different quantisation (FP8, NVFP4, INT4, Q4) or an online-quantised build answers differently, and the validators score it badly or strike it. Nothing in this release needs Blackwell-only formats.

## Several GPUs, big nodes

One hotkey (UID) serves one pool (several pools from block 9331987, see below) and has its own registration and public port. Inside a pool, weight = score × **verified capacity**, capped at the pool's target. Capacity is measured by surprise load probes (about one round in ten, at a time you cannot predict) that hit **all UIDs of a pool at the same moment**. So many hotkeys on one machine share that machine's throughput and add nothing, while one hotkey with more GPUs behind it counts more, up to the target. A UID that was never measured has capacity 0 until its first probe, which comes in the next round it answers. A bad answer is a strike and resets the moving average and the capacity. Give each miner its own GPU (do not share a GPU with other work) and its own public port.

### Several machines in different places behind one hotkey (opt-in)

Since subnet release 1.2.0rc9.post5, machines that are not in one private network can serve one hotkey (`s1-fast` and `s1-pro` only, off by default, `REAX_FEATURE_MULTINODE=1`). One small, stable **gateway** server runs the miner and is the only machine that holds the hotkey; it needs no GPU and should be close to the workers (within about 20–30 ms). Every **worker** runs the pinned runtime exactly as a single-machine miner does, plus `reax-runtime-relay`, which forwards signed requests from the gateway; workers never see the hotkey. Run the self-check on every worker before you add it, and firewall the relay port so only the gateway reaches it. Step-by-step guide: [docs/MINER.md, "Several machines in different places behind one hotkey"](https://github.com/reaxlabs/reax-subnet/blob/main/docs/MINER.md#several-machines-in-different-places-behind-one-hotkey-multinode-opt-in) · design and threat analysis: [docs/DESIGN-MULTINODE.md](https://github.com/reaxlabs/reax-subnet/blob/main/docs/DESIGN-MULTINODE.md). The bundled kit adds this when it moves to that release.

## Several models and a competition entry on one hotkey (from block 9331987)

From chain block **9331987** (about **13:00 UTC on 21 October 2026**, release 1.2.0rc10) one hotkey can

- serve **several pools** behind one public port (`REAX_MODELS`, for example `s1-lite,s1-cpu`), and
- hold **one competition entry** (use-case/generalist track or engine track) next to its inference commitment.

Before that block validators read neither, so keep one pool per hotkey until then. The miner refuses to start with two or more models before the block, and `reax-commit` refuses to write a second element before it.

What it does and does not change:

- Every model is scored as its own slot with its own pool cap, its own score and its own strikes, exactly like a separate hotkey. You save registrations, not hardware: each model still needs its own runtime on your machine, its own weights and its own free disk, and the pool hardware above applies per model.
- Each model has its own runtime (ports 8101 s1-fast, 8102 s1-pro, 8103 s1-lite, 8104 s1-cpu; loopback only, never published) and its own limits. The miner publishes one commitment, `reax-s1m/1:<pool>:<manifest_id>,<pool>:<manifest_id>`.
- `reaxctl install` still installs one pool. For several models use the example compose file in the bundled kit (kit 0.1.7, `service/docker-compose.multimodel.example.yml`) and follow [docs/MULTIMODEL.md](https://github.com/reaxlabs/reax-miner-kit/blob/main/docs/MULTIMODEL.md). In short: one runtime per model with the same token file, `REAX_MODELS=<pool>,<pool>` and `REAX_<POOL>_RUNTIME_URL=http://127.0.0.1:<port>` on the miner, started after the block.
- Write the competition entry with the tools in the miner image, never with a hand-made `btcli` commit, because every commitment write replaces all fields and would delete your inference commitment. With the miner's compose file (`C="docker compose -f <compose file> run --rm --no-deps"`):

```bash
$C --entrypoint reax-commit miner show                        # fields on chain and how validators read them
$C --entrypoint reax-commit miner set "reax-spec/1:<track_id>:<owner>/<repo>@<40-hex revision>" --dry-run
$C --entrypoint reax-commit miner set "reax-spec/1:<track_id>:<owner>/<repo>@<40-hex revision>"
$C --entrypoint reax-commit miner withdraw competition        # removes only the competition entry
```

  Run `--dry-run` first and read the fields it would write: the first one must be your inference commitment. The competition entry is evaluated on the subnet's own worker, never on your serving GPU. Track ids, deadlines and rules are on [reax.co/competitions](https://reax.co/competitions). Engine entries use `reax-engine-submit <image>@sha256:<digest>` in the same way once the engine track is open.
- The subnet documentation is the source of truth: [docs/MINER.md, "Several models on one hotkey"](https://github.com/reaxlabs/reax-subnet/blob/main/docs/MINER.md#several-models-on-one-hotkey-and-a-competition-entry-next-to-it) and [docs/DESIGN-MULTIROLE.md](https://github.com/reaxlabs/reax-subnet/blob/main/docs/DESIGN-MULTIROLE.md).

## Network

The miner needs a public IPv4 or IPv6 address with one inbound TCP port (default 8091). At home that means a port forward on your router. If a provider maps another external port, set `REAX_EXTERNAL_PORT` to it. Many rented "container pods" cannot run Docker or expose a fixed port; choose a VM or bare-metal server. See [rent a GPU](/rent).

## How your agent checks this

```bash
./reaxctl doctor --json
```

It reports the GPU, VRAM, driver, Docker, NVIDIA toolkit, disk, RAM, clock and ports, lists `eligible_pools` and gives a `fix` for every blocker. [Agent playbook](/agent.md) · [Rent a GPU](/rent) · [Troubleshooting](/troubleshooting)

# Rent a GPU for mining

{{HUMAN_NOTE}}

No suitable NVIDIA card at home? You can rent one by the hour or month. Your agent compares the options with you; **you** create the account, pay and start the server, then give the agent SSH access to it.

## What the rented server must offer

1. One NVIDIA GPU with **≥ 24 GB** per miner (see [hardware](/hardware)).
2. **Docker inside the server.** The miner runs two containers (miner and model sidecar). A VM or bare-metal server works; many "container pods" do not allow Docker inside.
3. **A reachable TCP port** from the internet. It does not have to be 8091: if the provider maps a different external port, the miner announces that one (`REAX_EXTERNAL_PORT`).
4. Linux, driver R580+ (CUDA 13), 32 GB RAM, 20 GB disk.

## Options (indicative prices, checked 12 October 2026)

Prices are list prices or live marketplace asks on that date, per GPU-hour unless stated, and change often. "Not confirmed" means we could not verify it from the provider's own documentation; check it before renting.

| Provider | EU? | Cards ≥ 24 GB | Indicative price | Docker inside / reachable port | Payment |
|---|---|---|---|---|---|
| [Lium](https://lium.io) (a Bittensor subnet) | hosts worldwide, choose by location | RTX 3090, 4090, 5090, A100, H100, H200, B200, B300 | RTX 3090 from ≈ $0.20, RTX 4090 ≈ $0.55, H100 ≈ $3.75 (live asks vary widely) | **Yes, tested by us**: we ran this miner on a Lium RTX 4090 pod with Docker; ports are forwarded host ports (external number differs) | card, stablecoin, **TAO or alpha** (`lium fund`) |
| [Hetzner](https://www.hetzner.com/dedicated-rootserver/matrix-gpu/) GPU servers | **EU** (Nuremberg, Falkenstein; Helsinki) | RTX PRO 6000 Blackwell 96 GB (GEX131); 24 GB RTX PRO 4000 (GEX45) | GEX131 from €889/month or ≈ €1.42/hour incl. IPv4 | yes: bare metal, root, public IPv4 | card, SEPA |
| [Scaleway](https://www.scaleway.com/en/pricing/gpu) | **EU** (Paris) | L4 24 GB, L40S 48 GB, H100, B300 | L4 €0.79/h, L40S ≈ €1.40/h, H100 PCIe ≈ €2.73/h | VM instances; Docker and public IP as on any Linux VM (not confirmed) | card |
| [UpCloud](https://upcloud.com/products/gpu-servers/) | **EU** (Helsinki and others) | L4, L40S, H100, B200 | H100 €1.79/h; L40S ≈ €1.62/h per GPU | VMs with root (Docker/public IP not confirmed on the GPU pages) | card |
| [Verda](https://verda.com) (formerly DataCrunch) | **EU** (Helsinki, Finland) | L40S, RTX PRO 6000, A100, H100, H200, B200, B300 | L40S ≈ $1.37, RTX PRO 6000 ≈ $1.89, H100 ≈ $3.25 (third-party comparison, 31 Aug 2026) | not confirmed | card |
| [OVHcloud](https://www.ovhcloud.com/en/public-cloud/gpu/) | **EU** | L4, L40S, H100 | H100 PCIe ≈ €2.80/h | VMs (not confirmed) | card |
| [RunPod](https://www.runpod.io) | some EU data centres | RTX 4090, 5090, L40S, A6000, H100 | RTX 4090 ≈ $0.34 (community) to $0.69 (secure) | **No**: pods cannot run your own Docker | card |
| [Vast.ai](https://vast.ai) | marketplace, per host | RTX 3090, 4090, 5090, A6000, L40S, H100 | marketplace asks | only **VM** offers allow Docker; Docker instances do not | card, crypto |
| [TensorDock](https://tensordock.com), [Genesis Cloud](https://www.genesiscloud.com), [Hyperstack](https://hyperstack.cloud), [Nebius](https://nebius.com), [Lambda](https://lambda.ai) | varies (Genesis, Hyperstack, Nebius have EU sites) | various | RTX 4090 from ≈ $0.35 (TensorDock); H100 ≈ $2–4 | not confirmed | card |

The L4 is not among the cards we measured; run the kit's self-check before serving on it.

## Quick picks

- **Cheapest that we know works:** a Lium RTX 3090 or 4090 pod (Docker works, port is forwarded). Can be paid in TAO.
- **EU-hosted, simple VM:** Scaleway L40S (Paris) or UpCloud L40S (Helsinki).
- **EU bare metal, monthly:** Hetzner GEX131 (96 GB, also fits a future 80–96 GB pool).
- **EU companies with their own data centre:** use your own hardware and see the [EU miner track](/eu).

Renting costs money whether or not the miner earns rewards. Compare the rent with your own expectations before you start, and stop the server when you stop mining. Prices on this page are not offers by us; we have no affiliation with these providers.

[Hardware](/hardware) · [Agent playbook](/agent.md)

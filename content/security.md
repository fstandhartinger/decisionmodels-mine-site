# Security: what runs, which rights, which network

Short answers for you and your security team, for kit {{KIT_VERSION}}:

* **How dangerous is it?** The miner runs as three small containers with your own user id, no Linux capabilities, a read-only root filesystem, one GPU and a private network namespace. Only the miner port is reachable from outside. Containers share the host kernel and the NVIDIA driver, like every GPU container.
* **How much software?** NVIDIA driver R580+, Docker Engine with the compose plugin, the NVIDIA Container Toolkit, Python 3.10+. Nothing else.
* **Which rights?** No sudo and no root. But whoever may talk to the Docker daemon is root-equivalent on that machine: use a dedicated machine, VM or service user (below).
* **What it never touches:** your coldkey and your wallet directory. Only the one hotkey file and the public `coldkeypub.txt` are mounted, read-only.

## What runs on the machine

| Component | Runs as | Capabilities | Root filesystem | Network | Mounts |
|---|---|---|---|---|---|
| `reaxctl` (kit script) | your user | none | n/a | outbound HTTPS only | its state directory (default `~/.reax-miner`) |
| `net` (idle network holder, pinned miner image) | your uid:gid | none, `no-new-privileges` | read-only | owns the private namespace; publishes only the miner port (default 8091) | none |
| `runtime` (model sidecar, pinned image) | your uid:gid | none, `no-new-privileges` | read-only, tmpfs `/tmp` | joins `net`; listens on that namespace's loopback only, not reachable from the host or the LAN | weights (read-only), runtime token (read-only), one GPU |
| `miner` (pinned image) | your uid:gid | none, `no-new-privileges` | read-only, tmpfs `/tmp` | joins `net`; serves the miner port; outbound to the Bittensor chain endpoint | the hotkey file and `coldkeypub.txt` (read-only) |

All images are pinned by digest in the release descriptor and built from the public `reax-subnet` source. Validators require the pinned runtime, so you cannot swap it for a "more secure" build without changing your answers and score.

## What to install

* NVIDIA driver R580 or newer (CUDA 13).
* Docker Engine with the compose plugin, and the NVIDIA Container Toolkit.
* Python 3.10+ with `venv` (for the kit's tool venv).

No other system service is needed. `reaxctl service install` adds a systemd **user** unit by default; it never asks for sudo.

## Which rights

**Docker group = root.** A user who can talk to the Docker daemon can start a privileged container and is therefore root-equivalent ([Docker docs](https://docs.docker.com/engine/install/linux-postinstall/)). The miner containers get no capabilities and cannot gain any, but the account that runs `reaxctl` can. Three ways to avoid handing that to a person's own account, least effort first:

1. A dedicated machine or VM that runs nothing else (recommended for companies).
2. A dedicated service user (`reax`) that alone is in the `docker` group; people use `sudo -u reax reaxctl ...`.
3. Rootless Docker for that user, with the NVIDIA toolkit in CDI or `no-cgroups` mode ([NVIDIA guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)). A container escape then lands as an unprivileged user.

Registration is paid and signed by a person in their own wallet; the kit cannot do it.

## What is exposed

* **Inbound:** only the miner port (default TCP 8091). Sidecar ports 8101, 8102 and 8000 are never published and, in the default layout, are not even reachable from the host.
* **Outbound:** HTTPS to the Bittensor chain endpoint, plus the model, image and kit downloads at install time. Outbound internet is otherwise open; restrict it with your own firewall if you need to.
* **Default layout (`--network-isolation bridge`):** a compromised sidecar cannot reach services on the host's loopback (databases, admin UIs), cannot write into its image, and sees exactly the one GPU you pinned with `--gpu`. `--network-isolation host` keeps the older host-network layout for hosts where Docker bridge networking is disabled; run only one miner per host there.
* Docker publishes the miner port itself, past host firewalls such as `ufw`. That is intended for the miner port only.

## Stronger isolation: options we evaluated (October 2026)

| Option | Gain over the default | Effort | Multi-GPU (8x B300) | Verdict |
|---|---|---|---|---|
| **Hardened containers (default)** | baseline | none | yes, one miner per GPU | **default** |
| Rootless Docker / Podman + CDI | daemon not root | medium | yes | documented option |
| gVisor `runsc` + nvproxy (`reaxctl install --isolation gvisor`) | user-space kernel for every container, filtered NVIDIA ioctls | medium: install runsc, one Docker config entry; driver must be on gVisor's list (R580 is) | one miner per GPU works; NVLink/NCCL not checked; B300 and 5090 not on its official list | optional profile, tested end to end: same answers, about 2 % slower |
| Firecracker microVM | strong VM boundary | n/a | n/a | **not possible today**: no released GPU/PCI passthrough |
| Kata Containers (VFIO) | VM boundary, GPU owned by the guest | high: Kubernetes, GPU Operator, IOMMU, bare metal | supported on HGX | for Kubernetes shops only |
| **Dedicated VM per miner** (QEMU/libvirt or a cloud VM with GPU passthrough) | VM boundary; the miner never sees your other systems | medium to high (IOMMU, vfio-pci, guest driver) | yes, one 8-GPU VM per node | **recommended for companies** |
| NVIDIA Confidential Computing | protects the guest from the host, the opposite direction | very high | yes (Blackwell) | not relevant for host protection |

RTX 5090 and RTX PRO 6000 (GB202) have a reported VFIO reset bug: after a VM shutdown the device can stay unresponsive until the host reboots. RTX 4090 and data-centre GPUs pass through normally. Isolation does not change scores: every option runs the same pinned CUDA image, and answers depend on GPU architecture, driver and CUDA build, not on the sandbox.

## Recommendation

1. **Everyone:** the kit's hardened default. Nothing to do.
2. **Companies with their own hardware (for example an 8x B300 node):** a dedicated machine or VM with the GPUs passed through, a service user, one miner per GPU (`reaxctl install --gpu N`), one hotkey each. The miner then has nothing of yours to reach.
3. **A sandbox kernel inside the machine, and you control the Docker daemon:** `reaxctl install --isolation gvisor` (the kit checks the gVisor setup and prints the steps if something is missing), then `reaxctl selfcheck`; a pass with the same distances means scores are unchanged.

## Measured (13 Oct 2026)

Two RTX 3090 on a rented node in Frankfurt and four RTX A6000 on a rented VM in the EU, driver 580.178.04, s1-fast pool, 640-item reference self-check with a SHA-256 over every returned probability:

* **Identical answers, bit for bit:** legacy host network, hardened default, and a second miner on GPU 1 all give the same hash and pass 640/640.
* **Same speed:** 25.4 decisions/s legacy, 25.3 hardened; 24.4 for the second miner running at the same time.
* **gVisor** (4x RTX A6000 VM): same answer hash as without gVisor, 32.5 vs 33.2 decisions/s, same start-up time.
* **Isolation held:** the sidecar port was not reachable from the host, a host-loopback listener was not reachable from the miner, writes outside `/tmp` failed, and each runtime saw exactly its one GPU.

**Not yet measured:** the s1-pro runtime (vLLM) under the read-only layout, and a registered miner serving validators on a real chain under the read-only layout. After registration run `reaxctl verify --selfcheck`; a file-system error in `reaxctl logs` is a bug to report.

[Hardware](/hardware) · [Agent playbook](/agent.md) · [Troubleshooting](/troubleshooting)

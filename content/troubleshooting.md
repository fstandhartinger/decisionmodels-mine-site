# Troubleshooting

{{PRACTICE_NOTE}}

Start with the read-only report. Each blocker includes a concrete fix for your machine.

```bash
./reaxctl doctor --json
./reaxctl plan --mode localnet --json
# Once setup is available and installed:
./reaxctl status --json
./reaxctl logs --lines 100
```

## Doctor blocker IDs

| Blocker | What to do |
| --- | --- |
| `gpu` | No usable NVIDIA GPU detected. Practice once source is public, or use a separately authorized Linux NVIDIA host |
| `driver` | Install a compatible R580+ NVIDIA driver with permission; use the Windows driver under WSL |
| `os` | Move real mining to Linux x86_64 or validate the conditional WSL2 path |
| `docker_client` | Install Docker Engine with approval |
| `docker_daemon` | Start Docker or grant user access with approval, then log out and back in |
| `compose` | Install the Docker Compose plugin |
| `toolkit` | Install NVIDIA Container Toolkit and configure the Docker runtime with approval |
| `ntp` | Enable OS time synchronization with approval; recheck NTP |
| `miner_port` | Resolve the conflicting listener or choose an unused miner port. Keep sidecars private |
| `cpu_cores`, `ram_gb` | Use a host meeting the release capacity or practice once source is public |
| `python` | Use Python 3.10+ for the bundled rehearsal |
| `gpu_capacity_s1-fast` | s1-fast needs a compatible NVIDIA GPU with 24 GB VRAM and R580+ |
| `gpu_capacity_s1-pro` | s1-pro needs 80–96 GB NVIDIA VRAM; this pool is not enabled at launch |
| `disk_s1-fast`, `disk_s1-pro` | Free space in your own REAX directory or choose a larger disk; follow the release's per-pool minimum |

## Exit codes

| Code | Meaning | Fix |
| --- | --- | --- |
| `0` | Command succeeded | Read warnings too; successful rehearsal is not mainnet readiness |
| `2` | Usage error | Read `./reaxctl spec --json` and correct arguments |
| `10` | Requirement unmet | Read `data.blockers` and their fixes |
| `11` | Needs a human | Complete only the listed human step; never share secrets |
| `12` | Not available yet | Wait for the source/images to be published at launch, or for live network availability; do not override the hold |
| `13` | Network/download failure | Check connection and pinned release; do not substitute arbitrary mirrors |
| `20` | Verification failed | Fix each failing checklist item, then rerun `verify` |
| `1` | Unexpected error | Keep a redacted diagnostic summary; consult the FAQ |

Never disable a firewall as a shortcut, publish model sidecars, copy coldkeys or improvise around the launch hold. A signing metadata failure is a stop, not permission for blind signing.

[REAX miner FAQ](https://reax.dev/miner-faq/) · [Agent playbook](/agent.md)

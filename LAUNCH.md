# REAX miner site launch checklist

Launch remains held until Florian gives GO. Do not announce or imply mining is live before that approval and verified release readiness.

1. Verify the kit/runtime release, public ingress, signing flow and pinned model/container checks. Preserve release review receipts. Confirm whether legacy `s1-fast` / `s1-pro` identifiers remain protocol pool IDs; use Decision Models in human branding.
2. Edit the kit's canonical release descriptor and `site/releases/current.json`: set `status.live`, the assigned `status.netuid`, `status.launch_status`, `images` and `source.public` to the verified values. Pin every image by its actual published digest, and source/model refs by immutable commit. Never guess a netuid or digest. Source-public-only practice must retain `status.live=false`.
3. Tag the reviewed kit release; run `python3 scripts/release-kit.py /path/to/reax-miner-kit` against that exact committed release to regenerate `kit.lock.json` and the archive. Run `python3 scripts/make-samples.py` to regenerate provenance if the pinned kit changed. Verify all release IDs, commits, archive hashes and digests agree.
4. Flip the approved GitHub repositories and GHCR images public. Verify anonymous repository, source archive and image access; confirm the actual digest matches the descriptor. Do not substitute mutable tags.
5. Update `https://reax.dev/miner.json` and the reax-site mining, registration and FAQ docs to the same release, netuid, status, image digests and supported platforms.
6. Remove the indexing hold by setting the single `INDEXING_ALLOWED` switch in `scripts/build.py` to `True`. Rebuild: this changes both HTML robots metadata and the nginx X-Robots-Tag header. Do not edit one independently.
7. Run `python3 scripts/build.py`, `python3 -m unittest discover -s tests`, `node tests/webmcp-check.js`, and `python3 scripts/check-headless.py`; review desktop/phone in both themes. Deploy through the lead's approved deployment path and verify live HTML, Markdown, manifest, descriptor, installer, archive checksum, 404 status and indexing headers.
8. Add the mining navigation link on `decisionmodels.io`, pointing to `https://mine.decisionmodels.io`.
9. Publish the announcement only with Florian's explicit GO, after live verification. No earnings claims.

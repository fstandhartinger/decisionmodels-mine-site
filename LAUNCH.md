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

## Additions after the final review (9 Oct 2026)
10. **Before step 4 (making source/images public):** audit the private `reax-subnet` repository history and every GHCR image layer for secrets, internal hostnames and unlicensed third-party code. Public source also needs `source.commit` (40-hex) in the descriptor: the kit refuses a public source without it.
11. **Trusted owners:** the kit accepts a fetched descriptor only if source and images belong to an owner listed in `reaxlib/descriptor.py` `TRUSTED_OWNERS` (today `fstandhartinger`). A move to a REAX organisation needs a new kit release first.
12. **No rollback of the flip for installed kits:** the kit refuses a descriptor that goes from live to not-live ("launch regression refused"). Double-check `status.live`/`netuid` before publishing; a mistake needs a new kit release.
13. **After the flip, re-run the evidence:** fresh-agent test with only the URL (harness `e2e/run-agent-e2e.sh` in the job folder), plus one real GPU run through the **pull-by-digest** path (the pre-launch GPU run built the images from source and never pulled).
14. **Repository visibility / stealth:** `reax-miner-kit` is private until launch (the playbook says so; the archive is served by the site). `decisionmodels-mine-site` is public because Coolify deploys it anonymously; make it private only together with a Coolify deploy key. Contact address everywhere is info@productivity-boost.com until Florian lifts the stealth rule. The playbook's `git clone` option and the "Kit source" links work only after the kit repository is public.
15. Step 5 edits reax.dev, which belongs to the REAX sites owner (workstream A / reax-site): coordinate there. Note: `reax.dev/mine/` and `miner.json` currently say every step can be rehearsed on a local chain; that is true only once the source is public.

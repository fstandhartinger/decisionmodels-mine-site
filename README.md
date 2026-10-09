# Decision Models mining entry point

Static, agent-first onboarding for `mine.decisionmodels.io`. Unpublished; indexing is held on all hosts. No deployment or runtime wallet actions are part of this repository.

## Build and review

Python 3.10+ is recommended for site development. The generated downloader accepts Python 3.8+; the bundled kit rehearsal needs 3.10+.

```sh
python3 -m pip install -r requirements.txt
python3 scripts/build.py
python3 -m unittest discover -s tests -v
node tests/webmcp-check.js
python3 scripts/check-headless.py
./scripts/serve-local.sh
```

Only the pinned `markdown` package is required to build. Unit tests and HTTP checks use Python's standard library. Node is optional for the read-only tool tests. Playwright is optional for browser checks. `scripts/screenshot.py` captures review screenshots with a disposable headless Chrome (`--isolated`) or an existing Chrome over CDP (`--cdp`).

```sh
python3 scripts/check-headless.py --screenshots /path/to/worker/shots
# Or against an already running preview:
python3 scripts/screenshot.py --url http://127.0.0.1:8088 --output /path/to/worker/shots
```

`serve-local.sh` serves plain static files; it does not implement Markdown negotiation or extensionless routes. Use nginx through `check-headless.py` to check actual routing. `screenshot.py` without `--url` starts a temporary loopback server that also resolves extensionless HTML routes.

## Release source and integrity

`content/agent.md` is lead-authored and preserved. Each page's HTML and Markdown twin come from the same `content/*.md` source. The landing has a custom shared template and generated progressive-enhancement features; its Markdown twin includes the same prompt variants, check output, requirements and key roles as text. Build-time placeholders are substituted from `kit.lock.json`.

Refresh the committed archive only from a clean committed kit repository:

```sh
python3 scripts/release-kit.py /path/to/reax-miner-kit
python3 scripts/make-samples.py
python3 scripts/build.py
```

This runs `git archive` at the exact HEAD, computes SHA-256, writes `kit.lock.json` and refreshes `site/releases/current.json` from that exact commit. Kit filenames and `kit.lock.json.version` use the literal semantic version from committed `reaxlib.__version__`; the subnet descriptor's `release_id` is a separate field. Missing or invalid kit semver fails before writing artifacts. Build refuses a checksum, subnet release or sample provenance mismatch. The archive is extracted without a containing directory; the installer refuses an existing destination and never executes the kit. It makes no network requests beyond this site's host and does not follow redirects. A co-hosted checksum is not an independently authenticated release signature.

The site descriptor is the source for onboarding status, requirements and pools; its registration status can be updated independently of the pinned kit archive. The build replaces only `status.notes` in the served descriptor and manifest with state-selected presentation copy. Chain state follows `status.live`; localnet rehearsal requires `source.public` (or an authorized `REAX_SOURCE_DIR`), while mainnet setup requires a live chain plus public source and images. Testnet also needs its own configured netuid. `mine.json` includes the ordered setup steps and human approval boundaries. Schema: `schemas/mine.schema.json`. WebMCP tools and the normal OS widget use the same manifest and requirement function. All tools are read-only; none runs a command or signs a transaction.

## Hosting

The Dockerfile builds with Python and serves via nginx 1.29 on port 8080. `/healthz` returns `ok`. HTML paths support `Accept: text/markdown` with `Vary: Accept`; explicit `.md` paths use `text/markdown`. CSP has only self-hosted scripts, styles and fonts. `robots.txt` deliberately allows fetching so agents can read held pages; the all-host `X-Robots-Tag: noindex, nofollow` controls the launch indexing hold.

`INDEXING_ALLOWED` in `scripts/build.py` is the **single switch** for HTML robots metadata and generated nginx headers. Keep it false until the release owner authorizes indexing. Rebuilding reads the current descriptor: `status.live` controls the chain status display, and `source.public` controls whether the public localnet rehearsal flow opens. Private source or images keep setup gated even after the chain reports live. Source-only availability permits localnet practice while real-network setup stays blocked.

## Content provenance and limits

OS/wallet/agent guidance comes from the lead's October 9 research. Windows REAX runtime, external networking and extension signing remain not yet tested by us end to end. No funded wallet signing or Ledger transaction was executed. The kit's Bittensor 11.1.0 pin differs from the research's current stable 11.3.0; the site documents that difference rather than silently changing pins.

`content/samples/doctor-*.txt` contains the real CLI text emitted by the pinned kit with its `core_4090.json` and `core_no_gpu.json` fixture inputs, injected as in `tests/test_core_doctor.py`. `scripts/make-samples.py` verifies the archive checksum, extracts to a temporary directory and calls the actual CLI offline with an isolated home. Both samples retain the complete doctor report. The 4090 sample has no tolerance or larger-pool warning; the no-GPU sample includes the private-source note and hardware blockers. `provenance.json` records the kit commit, archive, fixture and output hashes. Regenerate after changing kit pins. These are recorded sample machines, not a live miner. The animated hero session is explicitly illustrative.

Brand assets and fonts are copied unchanged from the supplied Decision Models kit. No third-party script, analytics, wallet bridge or registration UI runs here. Protocol/scoring/FAQ and registration link to reax.dev. Live Decision Models footer paths were read from the main site: `/legal/imprint` and `/legal/privacy`.

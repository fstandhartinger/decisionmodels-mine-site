#!/bin/sh
# Read this script before running. Downloads only from mine.decisionmodels.io.
set -eu
command -v python3 >/dev/null 2>&1 || { echo 'Python 3.8+ is required.' >&2; exit 1; }
python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)' || { echo 'Python 3.8+ is required.' >&2; exit 1; }
command -v tar >/dev/null 2>&1 || { echo 'tar is required.' >&2; exit 1; }
if command -v curl >/dev/null 2>&1; then downloader=curl
elif command -v wget >/dev/null 2>&1; then downloader=wget
else echo 'curl or wget is required.' >&2; exit 1; fi
if command -v sha256sum >/dev/null 2>&1; then verifier=sha256sum
elif command -v shasum >/dev/null 2>&1; then verifier=shasum
else echo 'sha256sum or shasum is required.' >&2; exit 1; fi
kit_dir=${REAX_KIT_DIR:-$HOME/reax-miner-kit}
# Never overwrite a prior checkout or key-bearing directory.
if [ -e "$kit_dir" ]; then echo "Destination already exists: $kit_dir" >&2; exit 1; fi
scratch=$(mktemp -d)
trap 'rm -rf "$scratch"' 0
trap 'exit 1' 1 2 3 15
archive="$scratch/{{KIT_TARBALL}}"
url='https://mine.decisionmodels.io/kit/{{KIT_TARBALL}}'
if [ "$downloader" = curl ]; then
  curl --fail --silent --show-error --proto '=https' --output "$archive" "$url"
else
  wget --https-only --max-redirect=0 -q -O "$archive" "$url"
fi
if [ "$verifier" = sha256sum ]; then actual=$(sha256sum "$archive")
else actual=$(shasum -a 256 "$archive"); fi
actual=${actual%% *}
if [ "$actual" != '{{KIT_SHA256}}' ]; then
  echo 'Checksum mismatch. Nothing extracted.' >&2
  exit 1
fi
mkdir -p "$kit_dir"
tar -xzf "$archive" -C "$kit_dir"
printf 'Verified kit {{KIT_VERSION}}. Next: cd "%s" && ./reaxctl doctor --json\n' "$kit_dir"
# Checksum integrity is not an independent release signature. Review the pinned source.
# Rehearsal requires Python 3.10+; this downloader only requires Python 3.8+.
# No sudo, streamed execution, wallet access or payments.
# Preserve the archive hash when reviewing the pinned release.

#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
python3 scripts/build.py
exec python3 -m http.server "${PORT:-8088}" --bind 127.0.0.1 --directory dist

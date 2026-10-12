#!/bin/sh
# Runs the EU-miner API (unprivileged, loopback) and nginx; if either dies the container exits
# so the platform restarts it.
set -eu
su-exec api:api /opt/venv/bin/python -m mine_eu &
api_pid=$!
nginx -g 'daemon off;' &
nginx_pid=$!
trap 'kill $api_pid $nginx_pid 2>/dev/null || true; wait; exit 0' TERM INT
while kill -0 "$api_pid" 2>/dev/null && kill -0 "$nginx_pid" 2>/dev/null; do
  sleep 1
done
echo "entrypoint: a child process exited; stopping container" >&2
kill "$api_pid" "$nginx_pid" 2>/dev/null || true
exit 1

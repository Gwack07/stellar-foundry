#!/usr/bin/env bash
# Run every offline check. Used by CI and before any push.
set -euo pipefail
cd "$(dirname "$0")/.."
tools/fetch_sources.sh .cache/src >/dev/null
python3 -I tools/validate2.py pack .cache/src
for f in pack/kubejs/*/*.js; do node --check "$f"; done
node tools/scope_test.js pack/kubejs/server_scripts >/dev/null && echo "server scripts load together: ok"
# index must be up to date
cp pack/index.toml /tmp/index.before; cp pack/pack.toml /tmp/pack.before
python3 tools/build_pack.py --index >/dev/null
if ! cmp -s pack/index.toml /tmp/index.before || ! cmp -s pack/pack.toml /tmp/pack.before; then
  echo "pack/index.toml was stale - run: python3 tools/build_pack.py --index"; exit 1
fi
echo "index up to date: ok"

#!/usr/bin/env bash
# Shallow, pinned clones of the mod sources the generator and validator read
# (recipe JSON, lang files, registry code). Usage: tools/fetch_sources.sh [dest=.cache/src]
set -euo pipefail
DEST="${1:-.cache/src}"
mkdir -p "$DEST"
fetch() { # name url commit [sparse paths...]
  local name=$1 url=$2 rev=$3; shift 3
  local dir="$DEST/$name"
  if [ -d "$dir/.git" ] && [ "$(git -C "$dir" rev-parse HEAD)" = "$rev" ]; then return; fi
  rm -rf "$dir"; git init -q "$dir"; git -C "$dir" remote add origin "$url"
  if [ $# -gt 0 ]; then git -C "$dir" sparse-checkout set --no-cone "$@"; fi
  git -C "$dir" fetch -q --depth 1 --filter=blob:none origin "$rev"
  git -C "$dir" checkout -q FETCH_HEAD
  echo "fetched $name @ ${rev:0:8}"
}
fetch create    https://github.com/Creators-of-Create/Create.git              7ff2760e4924d35d4bc2e22c4b19923f0178cd16 \
  /src/generated/resources/data/create/recipe/ /src/generated/resources/assets/create/lang/en_us.json /src/generated/resources/data/c/tags/
fetch ae2       https://github.com/AppliedEnergistics/Applied-Energistics-2.git db17504a86128fdf3dae31f5fb7a112a646e0b93 \
  /src/generated/resources/data/ae2/recipe/network/blocks/controller.json
fetch northstar https://github.com/Astronauts-of-Create/Northstar-Redux.git   b5def570b206e0f34477d51020e6b03e1cf2eebe \
  /src/main/java/com/lightning/northstar/content/ /src/main/resources/data/northstar/dimension/
fetch aero      https://github.com/Creators-of-Aeronautics/Simulated-Project.git 3705df2062bebba42c3ab3d6b3dd09faa1512850 \
  /aeronautics/common/src/generated/resources/assets/aeronautics/lang/en_us.json /simulated/common/src/generated/resources/assets/simulated/lang/en_us.json

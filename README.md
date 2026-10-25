# Stellar Foundry

A Factorio-style space modpack for Minecraft **1.21.1 / NeoForge 21.1.264**: Create factories,
science packs, branching tech, your own spaceships (Create Aeronautics + AeroStar), and the
Northstar planets. Player-facing guide: [docs/PLAYER_GUIDE.md](docs/PLAYER_GUIDE.md).

## Layout

| Path | What | Edit how |
|---|---|---|
| `pack/` | The packwiz pack: everything a player's instance receives | see below |
| `pack/mods/*.pw.toml` | One file per mod: exact version, download URL, hash | by hand / `packwiz` |
| `pack/kubejs/`, `pack/config/ftbquests/` | **Generated**: scripts, recipes, textures, quests | edit `tools/`, then regenerate |
| `pack/index.toml`, `pack/pack.toml` | packwiz index and hashes | `python3 tools/build_pack.py --index` |
| `tools/build2.py`, `tools/quests2.py` | Generator: science packs, gated recipes, items, quests | Python |
| `tools/scripts/*.js` | Custom KubeJS mechanics (pollution, weather, starter kit) | JS |
| `tools/validate2.py`, `tools/check.sh` | Offline checks: every ID vs. mod sources, JSON/SNBT, script scope | |
| `mods-src/stellar-core/` | Our own Java mod (NeoForge MDK) | Gradle, built by CI |
| `.github/workflows/` | CI: offline checks, headless server boot test, Java build | |

## Workflow

```bash
python3 tools/build_pack.py   # regenerate pack/ from tools/ (fetches pinned mod sources into .cache/)
tools/check.sh                # all offline checks - run before every commit
git commit && git push        # CI boots a real server with the pack and fails on any error
```

Players' Prism instances run `packwiz-installer-bootstrap` as a pre-launch command, so every
launch syncs mods, scripts, recipes and quests from `main`.

## Adding a mod

Add `pack/mods/<slug>.pw.toml` (copy the format of an existing one: Modrinth `url` + `sha512`, or
CurseForge `metadata:curseforge` + `file-id`/`project-id`), set `side` correctly
(`both` / `client` / `server`), run `python3 tools/build_pack.py --index`, push, and wait for CI.
With the packwiz CLI: `cd pack && packwiz modrinth add <slug>`.

# Notes for Claude working on Stellar Foundry

Owner: Peter. Plays via Prism Launcher on a MacBook. Medium-difficulty, Create-centred, non-linear
("branching but free") progression. Read README.md for layout; this file is conventions and traps.

## Hard constraints
- Minecraft 1.21.1, NeoForge 21.1.264. Don't change without being asked.
- **Northstar must stay at 0.5.4+1.21.1** - AeroStar 1.0.1 is built against exactly that. Never bump it.
- Don't add: Iris/shaders (Aeronautics visual bugs), Entity Culling (players vanish from Sable ships
  in multiplayer), Sound Physics Remastered (conflicts with Sound Physics: Aeronautics).
- Sodium is OK only at >= 0.8.12 release (earlier alphas crash with Aeronautics).
- Every ID used in recipes/quests/scripts must be verified against mod sources or jars - run
  `tools/check.sh`. Never guess registry names.

## Progression design (keep it non-linear)
- Kinetic science -> Blaze Burner -> four Earth branches (Logistic, Chemical, Aeronautical,
  Industrial/TFMG). Astronomy Table needs ANY TWO DIFFERENT branches (one recipe per pair).
- First space trip is a Northstar rocket: AeroStar's Dimensional Drive needs lunar sapphire (Moon).
- After the Moon, Mars/Venus/Mercury in any order; Warp Drive Core needs any two different planets.
- "Any of a set" = alternative recipes per combination, or the item tag `stellar:earth_branch_packs`.
- Planet physics (gravity/air) comes from AeroStar's own dimension_physics - don't override it.

## KubeJS traps we have hit (KubeJS 2101 / Rhino)
- All server scripts share ONE global scope. Prefix every top-level name per file
  (ORB_, POL_, WX_ ...). `tools/scope_test.js` simulates this.
- Do NOT wrap scripts in an IIFE: Rhino mis-handles `const` inside it ("redeclaration of var").
  Use `var` inside functions.
- Many vanilla methods are renamed for JS: `level.getTime()` (not getGameTime),
  `level.getDimensionKey()`, `level.getEntities()` is KubeJS's EntityArrayList. Check the
  `@RemapForJS` / `kjs$` names in KubeJS source (`core/mixin/*.java`, `core/*KJS.java`).
- ItemEntity.getItem() returns null when empty.
- Use colour codes (`§c`) in strings rather than Text.* helpers.

## Testing
- `tools/check.sh` offline; CI `server-smoke-test` boots a dedicated server with the full pack.
- On Peter's Mac the instance is at ~/Documents/prisminstances/StellarFoundry; logs in
  minecraft/logs (kubejs/*.log). Expect "Loaded 5/5 KubeJS server scripts ... 0 errors" and
  "removed 7 recipes ... 0 failed recipes".
- Quests edited in-game with the FTB editor are overwritten on next launch by the synced pack -
  port such edits back into tools/quests2.py.

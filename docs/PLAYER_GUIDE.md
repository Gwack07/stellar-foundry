# Stellar Foundry

A Factorio-style space modpack for **Minecraft 1.21.1 (NeoForge)**. Build a Create factory, research science packs, **design and fly your own spaceship** with Create Aeronautics, and explore the Moon, Mars, Venus and Mercury, then build the **Warp Drive Core**.

## Install (Prism Launcher)

1. In Prism, click **Add Instance → Import** and choose this folder (or `StellarFoundry.zip`).
2. Select the instance, then **Edit → Mods → Download mods**.
3. On the **Modrinth** tab, tick every mod below. For **Northstar**, open its version dropdown and pick **0.5.4+1.21.1**. Prism fills in dependencies (Sable, Geckolib, Rhino and so on) automatically.
4. On the **CurseForge** tab, tick FTB Quests and FTB Chunks (both NeoForge).
5. **Review and confirm → OK**, then launch.

> **Deliberately left out:** Iris shaders (visual bugs with Aeronautics) and Entity Culling (players vanish from ships in multiplayer).

> ⚠️ **Northstar must be 0.5.4.** AeroStar is built against exactly that version, and newer Northstar (0.6.x) will break or crash it. Don't click "Update all" on Northstar.

The instance is set to 8 GB RAM. Lower it under **Edit → Settings → Java** if your machine has 16 GB or less.

### Modrinth

| Mod | Version | Role |
|---|---|---|
| Create | latest 1.21.1 (6.0.10) | Factory core: belts, presses, sequenced assembly |
| Create Aeronautics | latest (1.3.x) | Build physics-simulated aircraft and ships (includes Sable) |
| Create: Northstar – Redux | **0.5.4+1.21.1** | Planets, titanium chemistry, oxygen, rockets |
| Create: AeroStar Northstar Comp | latest (1.0.1) | Flies your Aeronautics ships to Northstar planets and orbit |
| KubeJS | latest | Runs the pack's science packs, recipes and orbital mechanic |
| Applied Energistics 2 | latest | Optional mid-game storage network |
| Just Enough Items (JEI) | latest | Recipe viewer: every custom recipe is shown here |
| Jade | latest | Shows what you're looking at |
| ModernFix, FerriteCore | latest | Performance |
| Create: The Factory Must Grow (TFMG) | 1.2.0 | Oil, refining, steel, plastics, engines (the Industrial branch) |
| Sodium | 0.8.13 (release) | FPS. Works with Aeronautics 1.3+ and Sable 2.0+ per Sodium's notes |
| ImmediatelyFast | latest | Faster HUD/text rendering |
| Sound Physics: Aeronautics | latest | Echoes and muffling, including on moving ships. **Don't** add Sound Physics Remastered alongside it |
| AmbientSounds | latest | Atmosphere (pulls in CreativeCore) |
| Xaero's Minimap + World Map | latest | Navigation |
| Tectonic | latest | Bigger, more dramatic overworld terrain (pulls in Lithostitched) |

### CurseForge

| Mod | Role |
|---|---|
| FTB Quests (NeoForge) | The quest book |
| FTB Chunks (NeoForge) | Force-load stations and outposts so they run while you're away |

## How progression works

The tech tree branches instead of running in one straight line.

```
                  ┌── Logistic ──┐
Kinetic → Blaze ──┼── Chemical ──┼─ any 2 → Astronomy Table → Orbit → Moon → Lunar → Navigator
                  └─ Aeronautical┘                                                    │
                                                              ┌── Mars ──┐            │
                                     Warp Drive Core ← any 2 ─┼── Venus ─┼────────────┘
                                                              └─ Mercury ┘
```

- **Earth branches:** pick any **two different** of Logistic, Chemical, Aeronautical and Industrial to unlock the Astronomy Table (star maps = space travel). There are six recipes, one per pair. The others are optional but have their own rewards (AE2, titanium, flight, oil and rocket fuel).
- **Planets:** after the Moon, the Interplanetary Navigator opens Mars, Venus and Mercury **in any order**. Each has a unique science pack and unlocks a different machine:
  - Mars → Electrolysis Machine (hydrogen, oxygen, better titanium)
  - Venus → Combustion Engine (high power)
  - Mercury → Solar Panel
- **Endgame:** the Warp Drive Core needs packs from **any two different planets**, Kinetic and Lunar packs, and Earth-branch packs of any kind.
- **Multiple routes everywhere:** fly your own AeroStar ship or build a Northstar rocket; make titanium chemically on Earth or mine it on the Moon; burn biofuel, hydrocarbon, hydrogen or methane.

| Pack | Made from (sequenced assembly) | Unlocks |
|---|---|---|
| Kinetic | Iron plate → water, saw, press | Blaze Burner |
| Logistic | Gold sheet + electron tube, belt, brass | AE2 Controller; counts toward the Astronomy Table |
| Chemical | Titanium sheet + liquid carbon, salt | Counts toward the Astronomy Table |
| Aeronautical | Iron plate + gyro mechanism, propeller, envelope | Counts toward the Astronomy Table |
| Industrial | Cast iron sheet + steel mechanism, plastic sheet, coal coke | Counts toward the Astronomy Table |
| Lunar | Titanium sheet + lunar sapphire, vacuum crystal, moon sand | Interplanetary Navigator |
| Martian | Martian steel sheet + volcanic ash, martian iron, mars sand | Electrolysis Machine |
| Venusian | Titanium sheet + sulfuric acid, calorian log, venus stone | Combustion Engine |
| Mercurian | Tungsten sheet + shelf fungus, mercury stone, water | Solar Panel |

### Custom mechanics

- **Pollution and attacks:** furnaces, blaze burners, coke ovens and engines you place pollute their 64×64 area while running. Pollution slowly fades, but above 40 you get warnings, and above 80 hostile mobs (husks, spiders, vindicators) come for your factory. **Wear Engineer's Goggles and sneak** to see the local level. Knobs (thresholds, mob list, on/off) are at the top of `kubejs/server_scripts/pollution.js`.
- **Planet weather:** Mars gets dust storms (about 2 min in every 12: slowness and darkness), and Venus gets acid rain (about 3 min in every 10: poison). Being under a roof or seated protects you. Tune in `planet_weather.js`.
- **Starter kit:** first login gives the quest book, a wrench, goggles and food.

- **Orbital crystallisation:** polished rose quartz left on a floor in Earth orbit becomes a Vacuum Crystal after 30 s. You need it for Lunar science, so you need an automated line on a station.
- **Rocket first, then your own ship:** the first trip to the Moon is in a Northstar rocket. AeroStar's Dimensional Drive needs lunar sapphire, so once you're back with sapphire, any Aeronautics ship can become a spaceship.
- **Planet physics for ships** comes from AeroStar (gravity, air pressure, drag per world):

  | World | Gravity (vs Earth) | Air (vs Earth) | What it means for ships |
  |---|---|---|---|
  | Earth orbit | ~6% | none | Float freely; propellers useless |
  | Moon | ~16% | none | No propellers or balloons; use levitite or rockets |
  | Mars | ~37% | <1% | Propellers barely work |
  | Venus | ~89% | 92× | Balloons float easily; heavy drag |
  | Mercury | ~38% | none | Like the Moon |

## Tuning

- **Grind level:** each science recipe is in `kubejs/data/stellar/recipe/science/`. Change `"count"` for more or fewer packs per craft.
- **Gates:** `kubejs/data/stellar/recipe/gated/` holds the replacement recipes, and `kubejs/server_scripts/gating.js` lists which originals are removed. Delete a line there (and its JSON) to ungate that item.
- **Regenerating:** `tools/build2.py` regenerates everything (`python3 tools/build2.py <out> <mod-sources>`).

## If something breaks

The pack is built from the mods' source code but hasn't been play-tested yet. AeroStar in particular is a young mod. If you hit an error:

- Check `logs/kubejs/startup.log` and `logs/kubejs/server.log` in the instance folder.
- Missing recipe or "unknown item" usually means a mod version differs from the one listed above.

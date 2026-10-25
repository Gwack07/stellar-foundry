#!/usr/bin/env python3
"""Stellar Foundry v2 generator: Create + Create Aeronautics + Northstar 0.5.4 + AeroStar.

Usage: build2.py OUT_DIR SRC_DIR
Writes a complete Prism instance (configs, KubeJS, quests, textures) into OUT_DIR.
"""
import json, math, os, shutil, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT, SRC = sys.argv[1], sys.argv[2]
MC = os.path.join(OUT, "minecraft")
KJ = os.path.join(MC, "kubejs")
if os.path.exists(OUT):
    shutil.rmtree(OUT)

def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def wjson(path, obj):
    write(path, json.dumps(obj, indent=2) + "\n")

def load(rel):
    with open(os.path.join(SRC, rel), encoding="utf-8") as f:
        return json.load(f)

# ------------------------------------------------------------------ science packs
# key, name, colour, (tier label, where it comes from)
PACKS = [
    ("kinetic",      "Kinetic Science Pack",      (210, 60, 60),   "Earth - Create machinery"),
    ("logistic",     "Logistic Science Pack",     (60, 180, 75),   "Earth branch - brass and logistics"),
    ("chemical",     "Chemical Science Pack",     (60, 120, 216),  "Earth branch - titanium chemistry"),
    ("aeronautical", "Aeronautical Science Pack", (240, 200, 70),  "Earth branch - flight"),
    ("industrial",   "Industrial Science Pack",   (120, 120, 135), "Earth branch - oil, steel and plastics"),
    ("lunar",        "Lunar Science Pack",        (200, 200, 214), "The Moon"),
    ("martian",      "Martian Science Pack",      (200, 100, 45),  "Planet - Mars"),
    ("venusian",     "Venusian Science Pack",     (150, 210, 70),  "Planet - Venus"),
    ("mercurian",    "Mercurian Science Pack",    (160, 110, 220), "Planet - Mercury"),
]
EARTH_BRANCHES = ["logistic", "chemical", "aeronautical", "industrial"]
PLANETS = ["martian", "venusian", "mercurian"]

# ------------------------------------------------------------------ instance
write(os.path.join(OUT, "instance.cfg"), "\n".join([
    "[General]", "ConfigVersion=1.2", "InstanceType=OneSix", "name=Stellar Foundry",
    "iconKey=default", "OverrideMemory=true", "MinMemAlloc=2048", "MaxMemAlloc=8192",
    "notes=Factorio-style space pack: Create, Create Aeronautics, Northstar 0.5.4, AeroStar. See README.md.", "",
]))
wjson(os.path.join(OUT, "mmc-pack.json"), {
    "components": [
        {"uid": "net.minecraft", "version": "1.21.1", "important": True},
        {"uid": "net.neoforged", "version": "21.1.264"},
    ],
    "formatVersion": 1,
})
os.makedirs(os.path.join(MC, "mods"), exist_ok=True)

# ------------------------------------------------------------------ textures
def flask(colour, faded=False):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0)); px = img.load()
    out, glass = (30, 30, 40, 255), (220, 235, 245, 150)
    r, g, b = colour
    if faded:
        r, g, b = [int(c * 0.45 + 90) for c in (r, g, b)]
    liquid = (r, g, b, 255); dark = (int(r * .65), int(g * .65), int(b * .65), 255)
    light = (min(255, r + 60), min(255, g + 60), min(255, b + 60), 255)
    rows = {1: (6, 9), 2: (6, 9), 3: (6, 9), 4: (6, 9), 5: (6, 9), 6: (5, 10), 7: (4, 11),
            8: (3, 12), 9: (2, 13), 10: (2, 13), 11: (2, 13), 12: (2, 13), 13: (3, 12), 14: (4, 11)}
    fill_from = 10 if faded else 8
    for y, (a, z) in rows.items():
        for x in range(a, z + 1):
            if x in (a, z) or y in (1, 14):
                px[x, y] = out
            elif y >= fill_from:
                px[x, y] = dark if x >= z - 2 else liquid
            else:
                px[x, y] = glass
    if not faded:
        px[4, 9] = light; px[4, 10] = light; px[5, 9] = light
    for x in range(6, 10):
        px[x, 0] = (140, 95, 55, 255)
    return img

def crystal():
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0)); px = img.load()
    shape = ["......##........", ".....#bb#.......", ".....#bwb#..##..", "....#bbwb#.#bb#.",
             "....#bbbb##bwb#.", "...#bbbbbb#bbb#.", "...#bdbbbb#bbd#.", "..#bddbbbbb#d#..",
             "..#bddbbbbbb#...", "..#bdddbbbbb#...", "...#ddddbbb#....", "...#ddddddd#....",
             "....#ddddd#.....", ".....#####......"]
    cols = {"#": (60, 20, 70, 255), "b": (235, 130, 220, 255), "w": (255, 235, 255, 255), "d": (170, 70, 170, 255)}
    for y, row in enumerate(shape):
        for x, ch in enumerate(row):
            if ch in cols:
                px[x, y] = cols[ch]
    return img

def core():
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0)); px = img.load()
    for y in range(16):
        for x in range(16):
            d = math.hypot(x - 7.5, y - 7.5)
            if d < 7.2:
                if d > 6.0:
                    px[x, y] = (40, 40, 60, 255)
                elif d > 4.5:
                    i = int(((math.atan2(y - 7.5, x - 7.5) + math.pi) / (2 * math.pi)) * len(PACKS)) % len(PACKS)
                    px[x, y] = PACKS[i][2] + (255,)
                elif d > 2.5:
                    px[x, y] = (90, 200, 255, 255)
                else:
                    px[x, y] = (240, 255, 255, 255)
    return img

TEX = os.path.join(KJ, "assets", "kubejs", "textures", "item")
os.makedirs(TEX, exist_ok=True)
lang = {}
for key, name, col, _ in PACKS:
    flask(col).save(os.path.join(TEX, f"{key}_science_pack.png"))
    flask(col, True).save(os.path.join(TEX, f"incomplete_{key}_science_pack.png"))
    lang[f"item.kubejs.{key}_science_pack"] = name
    lang[f"item.kubejs.incomplete_{key}_science_pack"] = f"Incomplete {name}"
crystal().save(os.path.join(TEX, "vacuum_crystal.png"))
core().save(os.path.join(TEX, "warp_drive_core.png"))
lang["item.kubejs.vacuum_crystal"] = "Vacuum Crystal"
lang["item.kubejs.warp_drive_core"] = "Warp Drive Core"
wjson(os.path.join(KJ, "assets", "kubejs", "lang", "en_us.json"), lang)

# ------------------------------------------------------------------ recipe helpers
D = os.path.join(KJ, "data")
def item(i): return {"item": i}
def tag(t): return {"tag": t}
def fluid(f, mb): return {"type": "neoforge:single", "amount": mb, "fluid": f}
def ftag(t, mb): return {"type": "neoforge:tag", "amount": mb, "tag": t}
def P(k): return item(f"kubejs:{k}_science_pack")

def seq(key, base, steps, count=2):
    tr = f"kubejs:incomplete_{key}_science_pack"
    sequence = []
    for kind, arg in steps:
        if kind == "deploy":
            sequence.append({"type": "create:deploying", "ingredients": [item(tr), arg], "results": [{"id": tr}]})
        elif kind == "fill":
            sequence.append({"type": "create:filling", "ingredients": [item(tr), arg], "results": [{"id": tr}]})
        elif kind == "press":
            sequence.append({"type": "create:pressing", "ingredients": [item(tr)], "results": [{"id": tr}]})
        elif kind == "cut":
            sequence.append({"type": "create:cutting", "ingredients": [item(tr)], "results": [{"id": tr}], "processing_time": 50})
    res = {"id": f"kubejs:{key}_science_pack"}
    if count > 1:
        res["count"] = count
    wjson(os.path.join(D, "stellar", "recipe", "science", f"{key}_science_pack.json"), {
        "type": "create:sequenced_assembly", "ingredient": base, "loops": 1,
        "results": [res], "sequence": sequence, "transitional_item": {"id": tr}})

def shaped(path, pattern, key, result, count=1, mech=False):
    used = set("".join(pattern)) - {" "}
    assert used == set(key), (path, used ^ set(key))
    assert len({len(r) for r in pattern}) == 1, path
    r = {"type": "create:mechanical_crafting" if mech else "minecraft:crafting_shaped",
         "category": "misc", "key": key, "pattern": pattern, "result": {"count": count, "id": result}}
    if mech:
        r["accept_mirrored"] = False
    wjson(os.path.join(D, "stellar", "recipe", path + ".json"), r)

# ------------------------------------------------------------------ science pack recipes
# Kinetic: brass-free machines only (spout, saw, press) - brass is behind the Blaze Burner.
seq("kinetic", tag("c:plates/iron"), [("fill", fluid("minecraft:water", 100)), ("cut", None), ("press", None)], count=1)
# Earth branches (any order)
seq("logistic", tag("c:plates/gold"), [
    ("deploy", item("create:electron_tube")), ("deploy", item("create:belt_connector")),
    ("deploy", tag("c:ingots/brass")), ("press", None)])
seq("chemical", item("northstar:titanium_sheet"), [
    ("fill", ftag("c:carbon", 250)), ("deploy", item("northstar:salt")), ("press", None)])
seq("aeronautical", tag("c:plates/iron"), [
    ("deploy", item("simulated:gyroscopic_mechanism")), ("deploy", item("aeronautics:andesite_propeller")),
    ("deploy", item("aeronautics:white_envelope")), ("press", None)])
seq("industrial", item("tfmg:cast_iron_sheet"), [
    ("deploy", item("tfmg:steel_mechanism")), ("deploy", item("tfmg:plastic_sheet")),
    ("deploy", item("tfmg:coal_coke")), ("press", None)])
# Any Earth-branch pack (used by the Warp Drive Core so skipped branches stay optional)
wjson(os.path.join(D, "stellar", "tags", "item", "earth_branch_packs.json"),
      {"values": [f"kubejs:{k}_science_pack" for k in EARTH_BRANCHES]})
# Moon
seq("lunar", item("northstar:titanium_sheet"), [
    ("deploy", item("northstar:polished_lunar_sapphire")), ("deploy", item("kubejs:vacuum_crystal")),
    ("deploy", item("northstar:moon_sand")), ("press", None)])
# Planets (any order)
seq("martian", item("northstar:martian_steel_sheet"), [
    ("deploy", item("northstar:volcanic_ash_item")), ("deploy", item("northstar:raw_martian_iron_ore")),
    ("deploy", item("northstar:mars_sand")), ("press", None)])
seq("venusian", item("northstar:titanium_sheet"), [
    ("fill", ftag("c:sulfuric_acid", 250)), ("deploy", item("northstar:calorian_log")),
    ("deploy", item("northstar:venus_stone")), ("press", None)])
seq("mercurian", item("northstar:tungsten_sheet"), [
    ("deploy", item("northstar:mercury_shelf_fungus")), ("deploy", item("northstar:mercury_stone")),
    ("fill", fluid("minecraft:water", 250)), ("press", None)])

# ------------------------------------------------------------------ gated recipes
# Originals are removed by output+mod in server_scripts/gating.js; these replace them.
CR = "create/src/generated/resources/data/create/recipe/"
blaze = load(CR + "crafting/kinetics/empty_blaze_burner.json")
blaze["pattern"] = ["KIK", "IAI", "KIK"]; blaze["key"]["K"] = P("kinetic")
wjson(os.path.join(D, "stellar", "recipe", "gated", "empty_blaze_burner.json"), blaze)

ae = load("ae2/src/generated/resources/data/ae2/recipe/network/blocks/controller.json")
ae["pattern"] = ["aXa", "bcb", "aXa"]; ae["key"]["X"] = P("logistic")
wjson(os.path.join(D, "stellar", "recipe", "gated", "ae2_controller.json"), ae)

# Astronomy Table (star maps = space travel): any TWO DIFFERENT Earth branches.
astro_key = {"#": item("minecraft:paper"), "X": tag("minecraft:wooden_slabs"),
             "S": item("minecraft:iron_ingot"), "P": tag("c:stripped_logs")}
pairs = [(a, b) for i, a in enumerate(EARTH_BRANCHES) for b in EARTH_BRANCHES[i + 1:]]
for a, b in pairs:
    shaped(f"gated/astronomy_table_{a}_{b}", ["X#X", "ASB", "XPX"],
           dict(astro_key, A=P(a), B=P(b)), "northstar:astronomy_table")

# Interplanetary Navigator: needs Lunar science (one sapphire replaced by a pack)
shaped("gated/interplanetary_navigator", ["SLS", "CLC", "SNS", "CLC", "SLS", "T#T"], {
    "L": item("northstar:polished_lunar_sapphire"), "C": item("northstar:circuit"),
    "S": tag("c:plates/titanium"), "T": tag("c:ingots/titanium"),
    "#": item("northstar:targeting_computer"), "N": P("lunar")}, "northstar:interplanetary_navigator", mech=True)

# Planet unlocks - each planet teaches a different industry
shaped("gated/electrolysis_machine", ["MTPTM", "TCPCT", "PPLPP", "TCACT", "FFSFF"], {
    "A": item("northstar:amethyst_crystal"), "C": item("northstar:circuit"),
    "T": tag("c:plates/martian_steel"), "F": tag("c:ingots/martian_steel"),
    "P": item("create:fluid_pipe"), "L": item("create:fluid_tank"), "S": item("create:shaft"),
    "M": P("martian")}, "northstar:electrolysis_machine", mech=True)
shaped("gated/combustion_engine", ["PTP", "TCT", "AVA"], {
    "P": item("minecraft:piston"), "T": tag("c:plates/titanium"),
    "C": item("northstar:rocket_combustion_chamber"), "A": item("create:industrial_iron_block"),
    "V": P("venusian")}, "northstar:combustion_engine")
shaped("gated/solar_panel", ["GGG", "GGG", "MSM", "TCT", "TST"], {
    "G": item("minecraft:tinted_glass"), "S": item("create:shaft"), "T": tag("c:plates/titanium"),
    "C": item("northstar:circuit"), "M": P("mercurian")}, "northstar:solar_panel", mech=True)

# Warp Drive Core: any TWO DIFFERENT planets + everything from Earth and the Moon
for i, a in enumerate(PLANETS):
    for b in PLANETS[i + 1:]:
        shaped(f"endgame/warp_drive_core_{a}_{b}", [" KEK ", "ETNTE", "ATSTB", "ETNTE", " KEK "], {
            "K": P("kinetic"), "E": tag("stellar:earth_branch_packs"),
            "N": P("lunar"), "A": P(a), "B": P(b), "T": item("northstar:titanium_block"),
            "S": item("minecraft:nether_star")}, "kubejs:warp_drive_core", mech=True)

# Planet physics (gravity, air pressure, drag) come from AeroStar's own dimension_physics data.

# ------------------------------------------------------------------ scripts
pack_list = ",\n".join(f"  '{k}'" for k, *_ in PACKS)
write(os.path.join(KJ, "startup_scripts", "items.js"), f"""// Stellar Foundry - custom items
// Science packs are research currency: they go into the machines that unlock the next step.

const SCIENCE_PACKS = [
{pack_list}
]

StartupEvents.registry('item', event => {{
  SCIENCE_PACKS.forEach(key => {{
    event.create(`${{key}}_science_pack`).maxStackSize(64).rarity('uncommon')
    event.create(`incomplete_${{key}}_science_pack`).maxStackSize(1) // sequenced assembly
  }})
  event.create('vacuum_crystal').maxStackSize(64).rarity('rare')
  event.create('warp_drive_core').maxStackSize(1).rarity('epic').fireResistant()
}})
""")

gated = ["create:empty_blaze_burner", "ae2:controller", "northstar:astronomy_table",
         "northstar:interplanetary_navigator", "northstar:electrolysis_machine",
         "northstar:combustion_engine", "northstar:solar_panel"]
rm = "\n".join(f"  event.remove({{ output: '{o}', mod: '{o.split(':')[0]}' }})" for o in gated)
write(os.path.join(KJ, "server_scripts", "gating.js"), f"""// Stellar Foundry - remove the original recipes of gated machines.
// Their science-pack versions live in kubejs/data/stellar/recipe/gated (namespace 'stellar',
// so the mod filter below never removes them).

ServerEvents.recipes(event => {{
{rm}
}})
""")

write(os.path.join(KJ, "server_scripts", "orbital_crystal.js"), """// Stellar Foundry - Orbital Crystallisation
// Polished rose quartz left lying in Earth orbit grows into a Vacuum Crystal after 30 s.
// It only works in orbit, so players need a production line on a space station.

const ORB_ORBITS = ['northstar:earth_orbit']
const ORB_SEED_ITEM = 'create:polished_rose_quartz'
const ORB_RESULT_ITEM = 'kubejs:vacuum_crystal'
const ORB_GROW_TICKS = 600
let ORB_warned = false

ORB_ORBITS.forEach(dim => {
  LevelEvents.tick(dim, event => {
    const level = event.level
    if (level.isClientSide()) return
    // KubeJS exposes Level#getGameTime as getTime()
    if (level.getTime() % 20 != 0) return
    try {
      if (String(level.getDimensionKey().location()) !== dim) return
      level.getEntities().filterItems().forEach(entity => {
        const stack = entity.getItem() // null when empty
        if (stack == null || String(stack.getIdLocation()) !== ORB_SEED_ITEM) return
        const age = typeof entity.getAge === 'function' ? entity.getAge() : entity.age
        if (age < ORB_GROW_TICKS) return
        entity.setItem(Item.of(ORB_RESULT_ITEM, stack.getCount()))
      })
    } catch (e) {
      if (!ORB_warned) { console.error(`Orbital crystallisation failed in ${dim}: ${e}`); ORB_warned = true }
    }
  })
})
""")

tips = "\n".join(f"  event.add('kubejs:{k}_science_pack', ['\\u00a77{b}'])" for k, _, _, b in PACKS)
write(os.path.join(KJ, "client_scripts", "tooltips.js"), f"""// Stellar Foundry - tooltips and recipe-viewer notes

ItemEvents.modifyTooltips(event => {{
{tips}
  event.add('kubejs:vacuum_crystal', ['\\u00a7dGrown in Earth orbit from polished rose quartz'])
  event.add('kubejs:warp_drive_core', ['\\u00a76The way home... or further out.'])
}})

RecipeViewerEvents.addInformation('item', event => {{
  event.add('kubejs:vacuum_crystal', [
    'Drop Polished Rose Quartz on a floor in Earth orbit.',
    'After about 30 seconds in vacuum it crystallises into Vacuum Crystals.',
    'Automate it: a chute drops quartz onto a floor and a hopper below collects crystals.'
  ])
  event.add('northstar:astronomy_table', [
    'Needs science packs from any TWO different Earth branches:',
    'Logistic, Chemical, Aeronautical or Industrial. The others are optional.'
  ])
  event.add('kubejs:warp_drive_core', [
    'Needs packs from any TWO different planets: Mars, Venus or Mercury,',
    'plus Earth-branch packs of any kind.'
  ])
}})
""")

for f in ["pollution.js", "planet_weather.js", "starter_kit.js"]:
    with open(os.path.join(HERE, "scripts", f), encoding="utf-8") as fh:
        body = fh.read()
    write(os.path.join(KJ, "server_scripts", f), body)

# KubeJS server scripts share ONE global scope, so every top-level name is prefixed per file
# (ORB_, POL_, WX_). Don't wrap scripts in an IIFE: KubeJS's Rhino mishandles const inside it.

sys.path.insert(0, HERE)
import quests2
quests2.build(MC, write)
print("built", OUT)

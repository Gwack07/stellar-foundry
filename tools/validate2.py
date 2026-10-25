#!/usr/bin/env python3
"""Cross-check every ID in the v2 pack against the mods' sources. Usage: validate2.py PACK SRC"""
import json, os, re, sys

PACK, SRC = sys.argv[1], sys.argv[2]
# accept either a Prism instance (PACK/minecraft/...) or the packwiz root (PACK/kubejs/...)
MCDIR = PACK if os.path.isdir(os.path.join(PACK, "kubejs")) else os.path.join(PACK, "minecraft")
known = set()

def lang_ids(path, ns):
    for k in json.load(open(path, encoding="utf-8")):
        m = re.match(rf"^(item|block)\.{ns}\.([a-z0-9_]+)$", k)
        if m:
            known.add(f"{ns}:{m.group(2)}")

lang_ids(f"{SRC}/create/src/generated/resources/assets/create/lang/en_us.json", "create")
lang_ids(f"{SRC}/aero/aeronautics/common/src/generated/resources/assets/aeronautics/lang/en_us.json", "aeronautics")
lang_ids(f"{SRC}/aero/simulated/common/src/generated/resources/assets/simulated/lang/en_us.json", "simulated")
lang_ids(f"{MCDIR}/kubejs/assets/kubejs/lang/en_us.json", "kubejs")
# Northstar: registry names straight from its Registrate calls
ns_src = open(f"{SRC}/northstar/src/main/java/com/lightning/northstar/content/NorthstarItems.java").read() + \
         open(f"{SRC}/northstar/src/main/java/com/lightning/northstar/content/NorthstarBlocks.java").read()
for m in re.finditer(r'\.(?:item|block)\("([a-z0-9_]+)"', ns_src):
    known.add("northstar:" + m.group(1))
known |= {"tfmg:" + v for v in "cast_iron_sheet steel_mechanism plastic_sheet coal_coke coke_oven firebox blast_furnace_output regular_engine radial_engine large_engine simple_large_engine turbine_engine steel_distillation_controller pumpjack_base surface_scanner crude_oil_bucket diesel_bucket kerosene_bucket steel_ingot cast_iron_ingot".split()}
known |= {"kubejs:tab"}  # KubeJS creative tab (item/creativetab/KubeJSCreativeTabs.java)
known |= {"minecraft:slowness", "minecraft:darkness", "minecraft:poison", "minecraft:overworld"}
known |= {"ftbquests:book", "minecraft:bread", "minecraft:furnace", "minecraft:blast_furnace", "minecraft:smoker", "minecraft:husk", "minecraft:spider", "minecraft:vindicator", "minecraft:air", "minecraft:water"}
known |= {"aerostarcomp:dimensional_drive", "aerostarcomp:orbital_physics_assembler"}
known |= {"ae2:controller", "ae2:smooth_sky_stone_block", "ae2:fluix_crystal", "ae2:engineering_processor"}
known |= {"minecraft:" + v for v in ["nether_star", "paper", "iron_ingot", "piston", "tinted_glass",
                                      "netherite_leggings", "water", "lava"]}
FLUIDS = {"minecraft:water", "minecraft:lava"}
FLUID_TAGS = {"c:carbon", "c:sulfuric_acid"}
DIMS = {"northstar:" + d for d in os.listdir(f"{SRC}/northstar/src/main/resources/data/northstar/dimension")}
DIMS = {d[:-5] for d in DIMS}
TAGS = {"c:plates/iron", "c:plates/gold", "c:ingots/brass", "c:netherracks", "c:plates/titanium",
        "c:ingots/titanium", "c:plates/martian_steel", "c:ingots/martian_steel", "minecraft:wooden_slabs",
        "c:stripped_logs", "stellar:earth_branch_packs"}

problems = []
def chk(i, where):
    if i not in known:
        problems.append(f"unknown item {i} in {where}")

def walk(o, where):
    if isinstance(o, dict):
        t = o.get("type")
        if t == "neoforge:single":
            if o["fluid"] not in FLUIDS: problems.append(f"fluid {o['fluid']} in {where}")
            return
        if t == "neoforge:tag":
            if o["tag"] not in FLUID_TAGS: problems.append(f"fluid tag {o['tag']} in {where}")
            return
        for k, v in o.items():
            if k in ("item", "id") and isinstance(v, str):
                chk(v, where)
            elif k == "tag":
                if v not in TAGS: problems.append(f"unverified tag {v} in {where}")
            elif k == "dimension":
                if v not in DIMS: problems.append(f"dimension {v} in {where}")
            else:
                walk(v, where)
    elif isinstance(o, list):
        for x in o: walk(x, where)

n = 0
for root, _, files in os.walk(f"{MCDIR}/kubejs/data"):
    for f in files:
        p = os.path.join(root, f); d = json.load(open(p)); n += 1
        walk(d, os.path.relpath(p, MCDIR))
        if "pattern" in d:
            if len({len(r) for r in d["pattern"]}) != 1: problems.append(f"uneven rows {p}")
            used = set("".join(d["pattern"])) - {" "}
            if used != set(d["key"]): problems.append(f"key mismatch {p}")

qdir = f"{MCDIR}/config/ftbquests/quests"
nq = 0
for root, _, files in os.walk(qdir):
    for f in files:
        txt = open(os.path.join(root, f), encoding="utf-8").read()
        depth, instr, esc = 0, False, False
        for ch in txt:
            if instr:
                if esc: esc = False
                elif ch == "\\": esc = True
                elif ch == '"': instr = False
            elif ch == '"': instr = True
            elif ch in "{[": depth += 1
            elif ch in "}]": depth -= 1
        if depth or instr: problems.append(f"unbalanced SNBT {f}")
        for m in re.finditer(r'(?:item|icon): \{\s*id: "([^"]+)"', txt): chk(m.group(1), f)
        for m in re.finditer(r'dimension: "([^"]+)"', txt):
            if m.group(1) not in DIMS: problems.append(f"dimension {m.group(1)} in {f}")
        nq += txt.count('type: "') - txt.count('type: "xp"') - txt.count('type: "item"\n\t\t\t\t\t\titem') * 0

for root, _, files in os.walk(f"{MCDIR}/kubejs"):
    for f in files:
        if f.endswith(".js"):
            txt = open(os.path.join(root, f)).read()
            for m in re.finditer(r"'((?:create|northstar|kubejs|ae2|aeronautics|simulated|tfmg|minecraft|ftbquests):[a-z0-9_]+)'", txt):
                if m.group(1) not in known and m.group(1) not in DIMS:
                    problems.append(f"unknown id {m.group(1)} in {f}")

print(f"checked {n} data files; {len(known)} known ids; dims {sorted(DIMS)}")
print("\n".join(problems) if problems else "NO PROBLEMS")
sys.exit(1 if problems else 0)

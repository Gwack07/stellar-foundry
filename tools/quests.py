"""FTB Quests (1.21.1) quest book for Stellar Foundry. Imported by build.py (uses OUT/MC/write)."""
import hashlib, os

class D(float): pass       # SNBT double
class L(int): pass         # SNBT long

def qid(name):
    h = hashlib.sha1(("stellarfoundry:" + name).encode()).hexdigest()[:16].upper()
    if h[0] == "0":
        h = "1" + h[1:]
    return h

def esc(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'

def snbt(v, ind=0):
    pad = "\t" * ind
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, D):
        return f"{float(v)}d"
    if isinstance(v, L):
        return f"{int(v)}L"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, str):
        return esc(v)
    if isinstance(v, list):
        if not v:
            return "[ ]"
        inner = "\n".join(pad + "\t" + snbt(x, ind + 1) for x in v)
        return "[\n" + inner + "\n" + pad + "]"
    if isinstance(v, dict):
        if not v:
            return "{ }"
        inner = "\n".join(f"{pad}\t{k}: {snbt(x, ind + 1)}" for k, x in v.items())
        return "{\n" + inner + "\n" + pad + "}"
    raise TypeError(type(v))

# Quest spec: (key, title, [description lines], [tasks], [deps], x, y, [rewards])
# task: ("item", id, count, consume?) | ("dim", dimension) | ("check",)
# reward: ("xp", n) | ("item", id, count)

def I(i, n=1): return ("item", i, n)
def DIM(d): return ("dim", d)
CHECK = ("check",)

CHAPTERS = [
 ("spin_up", "Spin Up", "create:cogwheel", "Create machinery and your first science", [
  ("welcome", "Welcome to Stellar Foundry", [
     "Your goal: build a &6Warp Drive Core&r by researching every world in the solar system and beyond.",
     "",
     "Progress runs on &dscience packs&r. Each tier's packs are an ingredient in the machines and rocket parts that unlock the next tier.",
     "",
     "Hand-crafting will get you started. Automation will get you to the stars."],
   [CHECK], [], 0, 0, [("xp", 10)]),
  ("alloy", "Andesite Age", ["Mix andesite and iron nuggets to make Andesite Alloy, the backbone of early Create machinery."],
   [I("create:andesite_alloy", 16)], ["welcome"], 1.5, 0, [("xp", 25)]),
  ("water_wheel", "Free Rotation", ["A water wheel gives you steady rotational power. Stress units (SU) are your first 'power grid'."],
   [I("create:water_wheel")], ["alloy"], 3, -1, [("item", "create:shaft", 16)]),
  ("press", "Pressing Matters", ["The Mechanical Press flattens ingots into plates. Iron plates are the base of Kinetic Science."],
   [I("create:mechanical_press")], ["alloy"], 3, 1, [("xp", 50)]),
  ("line", "Assembly Line", ["A Spout and a Mechanical Saw over a belt, plus your press. Together they run &dsequenced assembly&r: items move down the belt and get processed step by step."],
   [I("create:spout"), I("create:mechanical_saw")], ["press"], 4.5, 1, [("xp", 50)]),
  ("belts", "Main Bus", ["Belts move items between machines. In Factorio terms, this is your main bus."],
   [I("create:belt_connector", 16)], ["water_wheel"], 4.5, -1, [("item", "create:andesite_casing", 8)]),
  ("kinetic_1", "Kinetic Science", [
     "Kinetic Science Packs are made by sequenced assembly on an iron plate:",
     "1. spout 100 mB water  2. saw  3. press.",
     "Put an iron plate on a belt under all three. Check JEI for the exact line."],
   [I("kubejs:kinetic_science_pack")], ["line", "belts"], 6, 0, [("xp", 100)]),
  ("kinetic_64", "Automate It", [
     "Build a line that makes packs without you: iron in one end, science out the other.",
     "Kinetic packs unlock the &6Blaze Burner&r, and with it, brass."],
   [I("kubejs:kinetic_science_pack", 64)], ["kinetic_1"], 7.5, 0, [("xp", 250)]),
 ]),

 ("brass_age", "Brass Age", "create:brass_ingot", "Heat, brass and logistics", [
  ("burner", "Bottled Fire", ["The Blaze Burner now needs Kinetic Science Packs. Catch a blaze and feed it fuel to heat mixers."],
   [I("create:empty_blaze_burner")], ["kinetic_64"], 0, 0, [("xp", 100)]),
  ("brass", "Brass", ["Heated mixing of copper and zinc makes brass. Automate it early: you'll need a lot."],
   [I("create:brass_ingot", 32)], ["burner"], 1.5, 0, [("xp", 100)]),
  ("tube", "Electron Tubes", ["Polished rose quartz plus an iron sheet. Needed for logistics science and brass machines."],
   [I("create:electron_tube", 16)], ["brass"], 3, -1, [("xp", 100)]),
  ("deployer", "Robot Hands", ["Brass makes the Brass Hand, and that makes the Deployer: it places items onto items mid-assembly."],
   [I("create:deployer", 3)], ["brass"], 3, 1, [("xp", 100)]),
  ("arm", "Inserters", ["The Mechanical Arm is Create's inserter. It needs a Precision Mechanism, your first long sequenced assembly."],
   [I("create:mechanical_arm")], ["deployer"], 4.5, 2, [("xp", 150)]),
  ("logistic_1", "Logistic Science", ["Sequenced assembly on a golden sheet: deploy an electron tube, a belt and a brass ingot, then press."],
   [I("kubejs:logistic_science_pack")], ["tube", "deployer"], 4.5, 0, [("xp", 150)]),
  ("logistic_64", "Scaling Up", ["Logistic packs unlock the Alternator, Electric Motor and Etrionic Blast Furnace. Time to electrify."],
   [I("kubejs:logistic_science_pack", 64)], ["logistic_1"], 6, 0, [("xp", 300)]),
 ]),

 ("electrification", "Electrification", "createaddition:alternator", "Power grids and steel", [
  ("alternator", "Generator", ["The Alternator turns rotation into Forge Energy (FE). Every Ad Astra machine runs on FE."],
   [I("createaddition:alternator")], ["logistic_64"], 0, 0, [("item", "createaddition:copper_spool", 8)]),
  ("wires", "Transmission Lines", ["Connectors and wire spools carry power across your base. Mind the distance."],
   [I("createaddition:connector", 4), I("createaddition:copper_spool", 4)], ["alternator"], 1.5, -1, [("xp", 100)]),
  ("blast", "Etrionic Blast Furnace", ["Alloys iron and coal into steel using power. Steel is the material of rocketry."],
   [I("ad_astra:etrionic_blast_furnace")], ["alternator"], 1.5, 1, [("xp", 150)]),
  ("steel", "Steel Industry", ["Automate steel. You will need hundreds of plates before you leave Earth."],
   [I("ad_astra:steel_ingot", 32)], ["blast"], 3, 1, [("xp", 150)]),
  ("compressor", "Compressor", ["Ad Astra's Compressor turns ingots into plates. A Create press works for iron, but rocket metals need this."],
   [I("ad_astra:compressor"), I("ad_astra:steel_plate", 16)], ["steel"], 4.5, 1, [("xp", 150)]),
  ("precision", "Precision Mechanisms", ["A five-loop sequenced assembly. Automate it: Electrical Science eats one per pack."],
   [I("create:precision_mechanism", 8)], ["wires"], 3, -1, [("xp", 150)]),
  ("capacitor", "Capacitors", ["Crafts & Additions capacitors store a little charge and go into Electrical Science."],
   [I("createaddition:capacitor", 8)], ["wires"], 4.5, -1, [("xp", 100)]),
  ("electrical_1", "Electrical Science", ["Sequenced assembly on a steel plate: capacitor, copper spool, precision mechanism, press."],
   [I("kubejs:electrical_science_pack")], ["compressor", "precision", "capacitor"], 6, 0, [("xp", 200)]),
  ("electrical_64", "Ready for Rocketry", ["Electrical packs unlock the NASA Workbench, where rockets are built."],
   [I("kubejs:electrical_science_pack", 64)], ["electrical_1"], 7.5, 0, [("xp", 400)]),
 ]),

 ("liftoff", "Liftoff", "ad_astra:tier_1_rocket", "Fuel, suits and the first rocket", [
  ("workbench", "NASA Workbench", ["The rocket assembly bench. Needs Electrical Science Packs."],
   [I("ad_astra:nasa_workbench")], ["electrical_64"], 0, 0, [("xp", 200)]),
  ("oil", "Black Gold", [
     "Rocket fuel is refined from oil. Find it in Overworld oceans, or make it:",
     "&eHeated mixing: 2 coal + 250 mB water -> 100 mB oil.&r",
     "Factorio veterans: this is your coal liquefaction."],
   [I("ad_astra:oil_bucket")], ["workbench"], 1.5, -1, [("xp", 100)]),
  ("refinery", "Fuel Refinery", ["Refines oil into fuel using power. Pipe it in and out for a continuous fuel line."],
   [I("ad_astra:fuel_refinery"), I("ad_astra:fuel_bucket")], ["oil"], 3, -1, [("xp", 150)]),
  ("suit", "Space Suit", ["Space has no air. Fill the suit's oxygen with an Oxygen Loader before launch."],
   [I("ad_astra:space_helmet"), I("ad_astra:space_suit"), I("ad_astra:space_pants"), I("ad_astra:space_boots"), I("ad_astra:oxygen_loader")],
   ["workbench"], 1.5, 1, [("xp", 150)]),
  ("rocket_1", "Tier 1 Rocket", ["Build it in the NASA Workbench, place it on a Launch Pad, fuel it, and climb aboard."],
   [I("ad_astra:launch_pad"), I("ad_astra:tier_1_rocket")], ["refinery", "suit"], 4.5, 0, [("xp", 300)]),
  ("orbit", "Low Earth Orbit", [
     "Fly to Earth Orbit and build a space station.",
     "This is your first &dspace platform&r: it's where Vacuum Crystals grow."],
   [DIM("ad_astra:earth_orbit")], ["rocket_1"], 6, -1, [("xp", 300)]),
  ("crystal", "Orbital Crystallisation", [
     "Drop &dPolished Rose Quartz&r on a station floor in any orbit.",
     "After about 30 seconds in vacuum it becomes a &dVacuum Crystal&r.",
     "Automate it: a chute or belt drops quartz onto the floor, a hopper underneath collects crystals.",
     "Remember to chunk-load the station (FTB Chunks) so it keeps running while you're away."],
   [I("kubejs:vacuum_crystal", 16)], ["orbit"], 7.5, -1, [("xp", 300)]),
  ("moon", "One Small Step", ["Land on the Moon. Bring oxygen, food, and a way home."],
   [DIM("ad_astra:moon")], ["rocket_1"], 6, 1, [("xp", 500)]),
 ]),

 ("lunar", "Lunar Outpost", "ad_astra:desh_ingot", "Desh, ice and the logistics network", [
  ("desh", "Desh", ["Desh ore is only found on the Moon. Mine it, smelt it, compress it into plates."],
   [I("ad_astra:raw_desh", 16), I("ad_astra:desh_plate", 8)], ["moon"], 0, 0, [("xp", 200)]),
  ("ice", "Lunar Ice", ["Ice shards from Moon ice ore. Also a source of water and oxygen later."],
   [I("ad_astra:ice_shard", 16)], ["moon"], 0, 2, [("xp", 100)]),
  ("cheese", "It Really Is Cheese", ["The Moon has cheese ore. Science demands a sample."],
   [I("ad_astra:cheese", 4)], ["moon"], 0, -2, [("item", "ad_astra:cheese", 16)]),
  ("outpost", "Outpost Power", [
     "Build a self-powered outpost: solar panels or a generator, plus oxygen distribution.",
     "Use FTB Chunks to claim and force-load the outpost so it runs while you're on Earth."],
   [I("ad_astra:solar_panel", 2), I("ad_astra:oxygen_distributor")], ["desh"], 1.5, 1, [("xp", 200)]),
  ("lunar_1", "Lunar Science", ["Sequenced assembly on a desh plate: ice shard, vacuum crystal, cheese, press."],
   [I("kubejs:lunar_science_pack")], ["desh", "ice", "cheese", "crystal"], 3, 0, [("xp", 300)]),
  ("lunar_64", "Interplanetary Supply Chain", [
     "Desh comes from the Moon, crystals from orbit, cheese from the Moon, power from Earth.",
     "Decide where to build. Ship materials with rockets, or build the line on site."],
   [I("kubejs:lunar_science_pack", 64)], ["lunar_1"], 4.5, 0, [("xp", 500)]),
  ("me", "Logistics Network", ["Lunar packs unlock the AE2 Controller: a full storage and autocrafting network. Your logistic robots have arrived."],
   [I("ae2:controller")], ["lunar_64"], 6, 1, [("xp", 300)]),
  ("rocket_2", "Tier 2 Rocket", ["The Desh Engine needs Lunar Science Packs. Tier 2 reaches Mars."],
   [I("ad_astra:desh_engine"), I("ad_astra:tier_2_rocket")], ["lunar_64"], 6, -1, [("xp", 500)]),
 ]),

 ("mars", "Red Planet", "ad_astra:ostrum_ingot", "Ostrum and a fuel economy", [
  ("mars", "Red Planet", ["Land on Mars. It's colder than it looks."],
   [DIM("ad_astra:mars")], ["rocket_2"], 0, 0, [("xp", 500)]),
  ("ostrum", "Ostrum", ["Martian ostrum, compressed into plates."],
   [I("ad_astra:raw_ostrum", 16), I("ad_astra:ostrum_plate", 8)], ["mars"], 1.5, -1, [("xp", 250)]),
  ("fuel_line", "Fuel Economy", ["Martian Science consumes rocket fuel. Scale your oil and refinery lines: 250 mB per pack."],
   [I("ad_astra:fuel_bucket", 8)], ["mars"], 1.5, 1, [("xp", 250)]),
  ("martian_1", "Martian Science", ["Sequenced assembly on an ostrum plate: fill with fuel, diamond, precision mechanism, press."],
   [I("kubejs:martian_science_pack")], ["ostrum", "fuel_line"], 3, 0, [("xp", 400)]),
  ("martian_64", "Martian Industry", ["Mars science unlocks the Ostrum Engine for Tier 3 rockets."],
   [I("kubejs:martian_science_pack", 64)], ["martian_1"], 4.5, 0, [("xp", 600)]),
  ("rocket_3", "Tier 3 Rocket", ["Tier 3 reaches Venus and Mercury."],
   [I("ad_astra:ostrum_engine"), I("ad_astra:tier_3_rocket")], ["martian_64"], 6, 0, [("xp", 600)]),
 ]),

 ("infernal", "Infernal Worlds", "ad_astra:calorite_ingot", "Venus, Mercury and heat", [
  ("venus", "Hell on a Planet", ["Venus is hot, crushing and full of calorite. Heat-proof yourself before landing."],
   [DIM("ad_astra:venus")], ["rocket_3"], 0, -1, [("xp", 600)]),
  ("mercury", "Closest to the Sun", [
     "Mercury has the strongest sunlight in the system (64 solar power vs Earth's 32).",
     "A solar farm here is the cheapest power in the game."],
   [DIM("ad_astra:mercury")], ["rocket_3"], 0, 1, [("xp", 600)]),
  ("calorite", "Calorite", ["Venusian calorite. Compress it into plates."],
   [I("ad_astra:raw_calorite", 16), I("ad_astra:calorite_plate", 8)], ["venus"], 1.5, -1, [("xp", 300)]),
  ("solar", "Solar Farm", ["Photovoltaic etrium cells go into solar panels and into Venusian Science."],
   [I("ad_astra:photovoltaic_etrium_cell", 8), I("ad_astra:mercury_cobblestone", 64)], ["mercury"], 1.5, 1, [("xp", 300)]),
  ("venusian_1", "Venusian Science", ["Sequenced assembly on a calorite plate: fill with lava, mercury cobblestone, etrium cell, press."],
   [I("kubejs:venusian_science_pack")], ["calorite", "solar"], 3, 0, [("xp", 500)]),
  ("venusian_64", "Two-World Factory", ["Calorite from Venus, stone from Mercury. Your supply chain now spans three planets."],
   [I("kubejs:venusian_science_pack", 64)], ["venusian_1"], 4.5, 0, [("xp", 800)]),
  ("rocket_4", "Tier 4 Rocket", ["The Calorite Engine needs Venusian Science. Tier 4 leaves the solar system."],
   [I("ad_astra:calorite_engine"), I("ad_astra:tier_4_rocket")], ["venusian_64"], 6, 0, [("xp", 800)]),
 ]),

 ("proxima", "Proxima", "kubejs:warp_drive_core", "Glacio and the Warp Drive Core", [
  ("glacio", "Proxima Centauri", ["Glacio orbits another star. It has air, but it's freezing."],
   [DIM("ad_astra:glacio")], ["rocket_4"], 0, 0, [("xp", 1000)]),
  ("permafrost", "Frozen Ground", ["Permafrost and glacian wood exist only on Glacio."],
   [I("ad_astra:permafrost", 32), I("ad_astra:glacian_log", 16)], ["glacio"], 1.5, -1, [("xp", 400)]),
  ("cryo", "Cryogenics", ["The Cryo Freezer turns ice into cryo fuel. Cryogenic Science needs 500 mB per pack."],
   [I("ad_astra:cryo_freezer"), I("ad_astra:cryo_fuel_bucket")], ["glacio"], 1.5, 1, [("xp", 400)]),
  ("cryogenic_1", "Cryogenic Science", ["Sequenced assembly on a calorite plate: cryo fuel, permafrost, vacuum crystal, glacian log, press."],
   [I("kubejs:cryogenic_science_pack")], ["permafrost", "cryo"], 3, 0, [("xp", 800)]),
  ("cryogenic_64", "Deep Space Industry", ["The last science tier. Stockpile every pack type for the final build."],
   [I("kubejs:cryogenic_science_pack", 64)], ["cryogenic_1"], 4.5, 0, [("xp", 1000)]),
  ("warp", "Warp Drive Core", [
     "A 5x5 mechanical crafting recipe using every science pack, calorite blocks and a nether star.",
     "Build it, and you've finished Stellar Foundry. Congratulations, engineer."],
   [I("kubejs:warp_drive_core")], ["cryogenic_64"], 6, 0, [("xp", 5000)]),
 ]),
]

def build_quests(MC, write):
    root = os.path.join(MC, "config", "ftbquests", "quests")
    write(os.path.join(root, "data.snbt"), snbt({
        "version": 13,
        "default_consume_items": False,
        "default_autoclaim_rewards": "disabled",
        "default_quest_shape": "circle",
        "default_quest_disable_jei": False,
        "disable_gui": False,
        "grid_scale": D(0.5),
        "title": "Stellar Foundry",
        "icon": {"id": "kubejs:warp_drive_core", "count": 1},
        "lock_message": "",
    }) + "\n")
    write(os.path.join(root, "chapter_groups.snbt"), snbt({"chapter_groups": []}) + "\n")

    ids = set()
    for ci, (ckey, ctitle, cicon, csub, quests) in enumerate(CHAPTERS):
        qlist = []
        for (key, title, desc, tasks, deps, x, y, rewards) in quests:
            q = {"id": qid("q:" + key), "title": title, "x": D(x * 2), "y": D(y * 2)}
            if desc:
                q["description"] = desc
            if deps:
                q["dependencies"] = [qid("q:" + d) for d in deps]
            tl = []
            for ti, t in enumerate(tasks):
                tid = qid(f"t:{key}:{ti}")
                if t[0] == "item":
                    tl.append({"id": tid, "type": "item", "item": {"id": t[1], "count": 1}, "count": L(t[2])})
                elif t[0] == "dim":
                    tl.append({"id": tid, "type": "dimension", "dimension": t[1]})
                elif t[0] == "check":
                    tl.append({"id": tid, "type": "checkmark"})
            q["tasks"] = tl
            rl = []
            for ri, r in enumerate(rewards):
                rid = qid(f"r:{key}:{ri}")
                if r[0] == "xp":
                    rl.append({"id": rid, "type": "xp", "xp": r[1]})
                else:
                    rl.append({"id": rid, "type": "item", "item": {"id": r[1], "count": 1}, "count": r[2]})
            if rl:
                q["rewards"] = rl
            if key in ("kinetic_64", "logistic_64", "electrical_64", "lunar_64", "martian_64", "venusian_64", "cryogenic_64", "warp"):
                q["size"] = D(1.5)
                q["shape"] = "gear"
            qlist.append(q)
            ids.add(key)
        chapter = {
            "id": qid("c:" + ckey),
            "group": "",
            "order_index": ci,
            "filename": ckey,
            "title": ctitle,
            "subtitle": [csub],
            "icon": {"id": cicon, "count": 1},
            "default_quest_shape": "",
            "default_hide_dependency_lines": False,
            "quests": qlist,
            "quest_links": [],
            "images": [],
        }
        write(os.path.join(root, "chapters", ckey + ".snbt"), snbt(chapter) + "\n")

    # sanity: every dependency references a defined quest
    allkeys = {q[0] for c in CHAPTERS for q in c[4]}
    for c in CHAPTERS:
        for q in c[4]:
            for d in q[4]:
                assert d in allkeys, (q[0], d)
    return CHAPTERS

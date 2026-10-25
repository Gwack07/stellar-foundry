"""Stellar Foundry v2 quest book (FTB Quests 1.21.1). Non-linear: branches + 'any N of M' gates."""
import os
from quests import D, L, qid, snbt

def I(i, n=1): return ("item", i, n)
def DIM(d): return ("dim", d)
CHECK = ("check",)

# quest: (key, title, desc_lines, tasks, deps, x, y, rewards, opts)
# opts: {"min": n} -> only n of the deps needed; {"big": True} -> milestone styling; {"optional": True}
def Q(key, title, desc, tasks, deps, x, y, rewards=None, **opts):
    return (key, title, desc, tasks, deps, x, y, rewards or [("xp", 50)], opts)

CHAPTERS = [
 ("spin_up", "1. Spin Up", "create:cogwheel", "Create basics and your first science", [
  Q("welcome", "Welcome to Stellar Foundry", [
    "Goal: build the &6Warp Drive Core&r.",
    "",
    "Progress runs on &dscience packs&r, made on Create assembly lines. Packs go into the machines that unlock the next step.",
    "",
    "The tech tree &obranches&r. On Earth, pick any two of four specialisations to reach space. Out in the solar system, visit the planets in any order, and any two will do for the endgame.",
    "",
    "&cWatch your pollution.&r Furnaces, blaze burners and engines pollute the air around them, and enough pollution draws attacks on your factory. Wear Engineer's Goggles and sneak to check the local level."
    "",
    "Hand-crafting gets you started. Automation gets you to the stars."],
    [CHECK], [], 0, 0, [("xp", 10)]),
  Q("alloy", "Andesite Age", ["Mix andesite with iron nuggets. Andesite alloy is the backbone of early Create."],
    [I("create:andesite_alloy", 16)], ["welcome"], 2, 0),
  Q("power", "Free Rotation", ["Water wheels and windmills give rotational power. Stress (SU) is your first power grid."],
    [I("create:water_wheel")], ["alloy"], 4, -1.5),
  Q("press", "Pressing Matters", ["The Mechanical Press flattens ingots into plates."],
    [I("create:mechanical_press")], ["alloy"], 4, 1.5),
  Q("belts", "Main Bus", ["Belts carry items between machines. In Factorio terms, this is your main bus."],
    [I("create:belt_connector", 16)], ["power"], 6, -1.5, [("item", "create:andesite_casing", 8)]),
  Q("line", "Assembly Line", ["A Spout and a Mechanical Saw over a belt, plus your press. Together they run &dsequenced assembly&r."],
    [I("create:spout"), I("create:mechanical_saw")], ["press"], 6, 1.5),
  Q("kinetic_1", "Kinetic Science", ["Sequenced assembly on an iron plate: spout 100 mB water, saw, press. Check JEI for the details."],
    [I("kubejs:kinetic_science_pack")], ["belts", "line"], 8, 0, [("xp", 100)]),
  Q("kinetic_64", "Automate It", [
    "Make packs without touching the line. Kinetic packs unlock the &6Blaze Burner&r, which means brass, heat and everything after it."],
    [I("kubejs:kinetic_science_pack", 64)], ["kinetic_1"], 10, 0, [("xp", 250)], big=True),
  Q("burner", "Bottled Fire", ["Catch a blaze. Heated mixing opens up brass and chemistry."],
    [I("create:empty_blaze_burner")], ["kinetic_64"], 12, 0, [("xp", 100)]),
 ]),

 ("branches", "2. Earth Branches", "northstar:titanium_ingot", "Pick any two of four - in any order", [
  Q("branches_intro", "Choose Your Specialisation", [
    "Four industries, four science packs. Space travel (the &6Astronomy Table&r) needs packs from &eany two different&r branches.",
    "",
    "&aLogistic&r: brass, trains and storage networks.",
    "&9Chemical&r: Northstar's titanium chemistry.",
    "&eAeronautical&r: physics-based flying machines.",
    "&7Industrial&r: oil wells, refineries, steel and plastics (TFMG).",
    "",
    "The rest are optional, but each has its own rewards."],
    [CHECK], ["burner"], 0, 0, [("xp", 25)]),
  # Logistic lane (top)
  Q("brass", "Brass", ["Heated mixing of copper and zinc."], [I("create:brass_ingot", 32)], ["branches_intro"], 2, -3),
  Q("tube", "Electron Tubes", ["Polished rose quartz plus an iron sheet."], [I("create:electron_tube", 16)], ["brass"], 4, -4),
  Q("deployer", "Robot Hands", ["Deployers place items onto items mid-assembly."], [I("create:deployer", 3)], ["brass"], 4, -2),
  Q("logistic_1", "Logistic Science", ["Sequenced assembly on a golden sheet: electron tube, belt and brass, then press."],
    [I("kubejs:logistic_science_pack")], ["tube", "deployer"], 6, -3, [("xp", 150)]),
  Q("logistic_64", "Logistics Specialist", ["A full stack of Logistic science. This also unlocks the &6AE2 Controller&r: your logistics robots."],
    [I("kubejs:logistic_science_pack", 64)], ["logistic_1"], 8, -3, [("xp", 300)], big=True),
  Q("me", "ME Network", ["Optional: a full storage and autocrafting network."], [I("ae2:controller")], ["logistic_64"], 10, -4, [("xp", 200)], optional=True),
  # Chemical lane (middle)
  Q("rutile", "Rutile", ["Crush sand, or better, limestone, for rutile concentrate (titanium ore)."],
    [I("northstar:rutile_concentrate", 16)], ["branches_intro"], 2, 0),
  Q("salt", "Salt of the Nether", ["Crush basalt for salt, then fill salt with lava to make a sodium catalyst."],
    [I("northstar:salt", 8), I("northstar:sodium_catalyst", 4)], ["branches_intro"], 2, 1.5),
  Q("titanium", "Titanium", [
    "Superheated mixing: 3 rutile, sodium catalyst, zinc and liquid carbon (compact coal) make titanium tetrachloride.",
    "Then a sturdy sheet goes through lava, TiCl4 and water fills with presses in between.",
    "A proper chemical plant: plan your pipes."],
    [I("northstar:titanium_ingot", 8)], ["rutile", "salt"], 4, 0.75, [("xp", 200)]),
  Q("chemical_1", "Chemical Science", ["Sequenced assembly on a titanium sheet: 250 mB liquid carbon, salt, press."],
    [I("kubejs:chemical_science_pack")], ["titanium"], 6, 0.75, [("xp", 150)]),
  Q("chemical_64", "Chemistry Specialist", ["A full stack of Chemical science."],
    [I("kubejs:chemical_science_pack", 64)], ["chemical_1"], 8, 0.75, [("xp", 300)], big=True),
  # Aeronautical lane (bottom)
  Q("assembler", "Physics Assembler", [
    "Create Aeronautics turns any structure into a simulated, physics-driven vehicle.",
    "Build a frame, place a Physics Assembler, and give it a signal."],
    [I("simulated:physics_assembler")], ["branches_intro"], 2, 4),
  Q("prop", "Propellers", ["Propeller bearings and propellers push air. Thrust depends on &eair pressure&r, so they weaken with altitude and on thin-air planets."],
    [I("aeronautics:propeller_bearing"), I("aeronautics:andesite_propeller", 4)], ["assembler"], 4, 3.25),
  Q("gyro", "Stable Flight", ["Gyroscopic mechanisms keep a craft level. Sequenced assembly with cogwheels, shafts and brass nuggets."],
    [I("simulated:gyroscopic_mechanism", 4)], ["assembler"], 4, 4.75),
  Q("first_flight", "First Flight", ["Build a craft that takes off, flies a lap and lands in one piece. Tick this when you have."],
    [CHECK], ["prop", "gyro"], 6, 4, [("xp", 150)]),
  Q("aeronautical_1", "Aeronautical Science", ["Sequenced assembly on an iron plate: gyroscopic mechanism, andesite propeller, white envelope, press."],
    [I("kubejs:aeronautical_science_pack")], ["prop", "gyro"], 6, 5.5, [("xp", 150)]),
  Q("aeronautical_64", "Aviation Specialist", ["A full stack of Aeronautical science."],
    [I("kubejs:aeronautical_science_pack", 64)], ["aeronautical_1"], 8, 5.5, [("xp", 300)], big=True),
  # Industrial lane (TFMG)
  Q("coke", "Coke Ovens", ["TFMG's coke oven turns coal into coal coke, the fuel for real steelmaking."],
    [I("tfmg:coke_oven"), I("tfmg:coal_coke", 16)], ["branches_intro"], 2, 8),
  Q("scanner", "Prospecting", ["The Surface Scanner finds underground &8oil deposits&r. Find one and build a pumpjack on it."],
    [I("tfmg:surface_scanner")], ["branches_intro"], 2, 9.5),
  Q("oil", "Black Gold", ["Pump crude oil. A pumpjack needs rotation and a deposit underneath."],
    [I("tfmg:pumpjack_base"), I("tfmg:crude_oil_bucket")], ["scanner"], 4, 9.5, [("xp", 150)]),
  Q("refinery", "Refinery", [
    "A steel distillation tower splits crude into diesel, gasoline, kerosene, naphtha and more.",
    "&eKerosene and diesel are rocket fuels&r for Northstar."],
    [I("tfmg:steel_distillation_controller"), I("tfmg:kerosene_bucket")], ["oil"], 6, 9.5, [("xp", 200)]),
  Q("steel", "Cast Iron and Steel", ["TFMG's blast furnace makes cast iron and steel."],
    [I("tfmg:cast_iron_ingot", 16), I("tfmg:steel_ingot", 16)], ["coke"], 4, 8),
  Q("industrial_1", "Industrial Science", ["Sequenced assembly on a cast iron sheet: steel mechanism, plastic sheet, coal coke, press."],
    [I("kubejs:industrial_science_pack")], ["steel", "refinery"], 8, 8.75, [("xp", 150)]),
  Q("industrial_64", "Industry Specialist", ["A full stack of Industrial science."],
    [I("kubejs:industrial_science_pack", 64)], ["industrial_1"], 10, 8.75, [("xp", 300)], big=True),
  Q("engine", "Diesel Power", ["Optional: TFMG engines burn fuel for big rotational power. They pollute, too."],
    [I("tfmg:regular_engine")], ["refinery"], 8, 10.5, [("xp", 200)], optional=True),
  Q("levitite", "Floating Rock", ["Levitite floats by itself instead of pushing air, so it's your lift source where there is no air (as far as the mod's docs show: test it before you rely on it)."],
    [I("aeronautics:levitite", 8)], ["first_flight"], 8, 4, [("xp", 200)], optional=True),
 ]),

 ("orbit", "3. Reaching Orbit", "northstar:star_map", "Star maps, spaceships and the first station", [
  Q("astronomy", "Astronomy Table", [
    "The Astronomy Table turns telescope readings into &bstar maps&r, your navigation data.",
    "It needs science packs from &eany two different&r Earth branches. There are six recipes, one per pair; JEI shows them all."],
    [I("northstar:astronomy_table")], ["logistic_64", "chemical_64", "aeronautical_64", "industrial_64"], 0, 0, [("xp", 300)], min=2, big=True),
  Q("telescope", "Look Up", ["Craft a telescope, put it under open sky and take &bastronomical readings&r with paper."],
    [I("northstar:telescope"), I("northstar:astronomical_reading", 4)], ["astronomy"], 2, -1.5),
  Q("star_map", "Chart the Moon", ["Combine readings at the Astronomy Table into a star map."],
    [I("northstar:star_map")], ["telescope"], 4, -1.5, [("xp", 150)]),
  Q("suit", "Suit Up", [
    "Space has no air. Northstar's iron space suit seals you in.",
    "An &6Atmospheric Concentrator&r pulls oxygen out of Earth's air, and an Oxygen Filler tops up your suit. Pipe it onto your ship too.",
    "For Venus later, Create's &6netherite diving gear&r is heat-proof."],
    [I("northstar:iron_space_suit_helmet"), I("northstar:iron_space_suit_chestpiece"),
     I("northstar:iron_space_suit_leggings"), I("northstar:iron_space_suit_boots")], ["astronomy"], 2, 1.5),
  Q("rocket_station", "Rocket Station", [
    "Your first trip off Earth has to be a &6Northstar rocket&r. The Dimensional Drive for custom ships needs lunar sapphire, which only exists on the Moon.",
    "",
    "The Rocket Station assembles a rocket from the blocks you build around it: hull, jet engines, fuel tanks, seats, and the star map for your destination. Ponder (hold W over it) shows the details."],
    [I("northstar:rocket_station")], ["star_map", "suit"], 6, 0, [("xp", 300)]),
  Q("ship", "Liftoff", ["Build, fuel and launch your rocket. Tick this when you're airborne."],
    [CHECK], ["rocket_station"], 7, 0, [("xp", 200)], big=True),
  Q("orbit", "Low Earth Orbit", ["Reach Earth orbit. Zero gravity: your ship floats, but you can still walk the deck."],
    [DIM("northstar:earth_orbit")], ["ship"], 8, -1.5, [("xp", 300)]),
  Q("station", "Space Station", [
    "Build a permanent station in orbit. FTB Chunks lets you force-load it so it keeps running while you're away."],
    [CHECK], ["orbit"], 10, -1.5, [("xp", 200)]),
  Q("crystal", "Orbital Crystallisation", [
    "Drop &dPolished Rose Quartz&r on a floor in Earth orbit. After 30 seconds in vacuum it becomes a &dVacuum Crystal&r.",
    "Automate it: a chute drops quartz onto a floor and a hopper below collects crystals."],
    [I("kubejs:vacuum_crystal", 16)], ["orbit"], 10, 0, [("xp", 300)]),
  Q("moon", "One Small Step", [
    "Point your rocket at the Moon star map and land.",
    "Moon gravity is about 1/6 of Earth's and there is &cno air&r: propellers and balloons do nothing here."],
    [DIM("northstar:moon")], ["ship"], 8, 1.5, [("xp", 500)], big=True),
 ]),

 ("moon", "4. Lunar Outpost", "northstar:polished_lunar_sapphire", "Sapphire, titanium and the way out", [
  Q("sapphire", "Lunar Sapphire", ["Sapphire geodes only grow on the Moon. Crush the clusters, then polish the shards with sandpaper."],
    [I("northstar:lunar_sapphire_shard", 16), I("northstar:polished_lunar_sapphire", 8)], ["moon"], 0, -1.5, [("xp", 200)]),
  Q("moon_sand", "Regolith", ["Moon sand. Also a slow source of liquid carbon."], [I("northstar:moon_sand", 32)], ["moon"], 0, 1.5),
  Q("moon_ti", "Titanium Ore", ["Skipped the Chemical branch? The Moon has &etitanium ore&r. Mine it instead of building a chemical plant."],
    [I("northstar:raw_titanium_ore", 16)], ["moon"], 0, 4, [("xp", 150)], optional=True),
  Q("drive", "Dimensional Drive", [
    "Lunar sapphire unlocks AeroStar's &6Dimensional Drive&r. Put one on any Create Aeronautics ship and it becomes a spaceship.",
    "Insert a star map (an empty slot means Earth orbit), climb past the required altitude shown on the drive, and the ship jumps, crew included.",
    "Remember: no air in space. Propellers die above the atmosphere and on airless worlds, so use levitite for lift there."],
    [I("aerostarcomp:dimensional_drive")], ["sapphire"], 2, -3, [("xp", 400)], big=True),
  Q("orbital_assembler", "Orbital Physics Assembler", [
    "Optional: assembles and disassembles physics structures in mid-air. Build space stations that you can dock to or turn into ships."],
    [I("aerostarcomp:orbital_physics_assembler")], ["drive"], 4, -3, [("xp", 200)], optional=True),
  Q("lunar_1", "Lunar Science", ["Sequenced assembly on a titanium sheet: polished sapphire, vacuum crystal, moon sand, press.",
    "Materials from the Moon &oand&r orbit, so you need a supply chain."],
    [I("kubejs:lunar_science_pack")], ["sapphire", "moon_sand", "crystal"], 2, 0, [("xp", 300)]),
  Q("lunar_64", "Lunar Industry", ["A full stack. Lunar science unlocks the &6Interplanetary Navigator&r."],
    [I("kubejs:lunar_science_pack", 64)], ["lunar_1"], 4, 0, [("xp", 500)], big=True),
  Q("navigator", "Interplanetary Navigator", [
    "Install it on your rocket or your Dimensional Drive ship to travel to other planets. The Moon doesn't need one.",
    "Mars, Venus and Mercury are all open now, in &eany order&r."],
    [I("northstar:interplanetary_navigator")], ["lunar_64"], 6, 0, [("xp", 500)]),
 ]),

 ("planets", "5. The Inner Planets", "northstar:martian_steel", "Three worlds, any order - each teaches a new industry", [
  Q("planets_intro", "Pick a Planet", [
    "Each planet has a unique science pack and unlocks a different machine:",
    "&6Mars&r: thin air, dust storms, martian steel, &6Electrolysis Machine&r (hydrogen, oxygen, better titanium).",
    "&6Venus&r: crushing heat, acid rain, thick air, &6Combustion Engine&r (serious power).",
    "&6Mercury&r: tungsten, blazing sun, &6Solar Panel&r.",
    "",
    "The Warp Drive Core needs science from &eany two&r of them."],
    [CHECK], ["navigator"], 0, 0, [("xp", 50)]),
  # Mars
  Q("mars", "Red Planet", ["Land on Mars. The air is under 1% of Earth's: propellers barely work, so lean on levitite or rockets."],
    [DIM("northstar:mars")], ["planets_intro"], 2, -3.5, [("xp", 500)]),
  Q("martian_steel", "Martian Steel", ["Compact titanium, raw martian iron and volcanic ash (heated)."],
    [I("northstar:martian_steel", 16), I("northstar:martian_steel_sheet", 8)], ["mars"], 4, -3.5),
  Q("martian_1", "Martian Science", ["Sequenced assembly on a martian steel sheet: volcanic ash, raw martian iron, mars sand, press."],
    [I("kubejs:martian_science_pack")], ["martian_steel"], 6, -3.5, [("xp", 400)]),
  Q("martian_64", "Martian Industry", ["Unlocks the Electrolysis Machine."], [I("kubejs:martian_science_pack", 64)], ["martian_1"], 8, -3.5, [("xp", 600)], big=True),
  Q("electrolysis", "Splitting Water", ["Water becomes oxygen and hydrogen, and brine becomes chlorine and sodium. Hydrogen is rocket fuel too."],
    [I("northstar:electrolysis_machine")], ["martian_64"], 10, -3.5, [("xp", 300)]),
  # Venus
  Q("venus_gear", "Heat-Proof", ["Venus is hot enough to cook you. Wear a full set of Create's netherite diving gear (Nether materials)."],
    [I("create:netherite_diving_helmet"), I("create:netherite_backtank"), I("minecraft:netherite_leggings"), I("create:netherite_diving_boots")],
    ["planets_intro"], 2, 0, [("xp", 300)]),
  Q("venus", "Hell on a Planet", ["Land on Venus. The atmosphere is 92 times Earth's, thick as soup. Balloons float easily, but expect heavy drag."],
    [DIM("northstar:venus")], ["venus_gear"], 4, 0, [("xp", 500)]),
  Q("acid", "Sulfuric Acid", ["Venus has sulfuric acid lakes. Pump some home. Also crush venus gravel: it's the richest rutile source in the system."],
    [I("northstar:calorian_log", 16), I("northstar:venus_stone", 32)], ["venus"], 6, 0),
  Q("venusian_1", "Venusian Science", ["Sequenced assembly on a titanium sheet: 250 mB sulfuric acid, calorian log, venus stone, press."],
    [I("kubejs:venusian_science_pack")], ["acid"], 8, 0, [("xp", 400)]),
  Q("venusian_64", "Venusian Industry", ["Unlocks the Combustion Engine."], [I("kubejs:venusian_science_pack", 64)], ["venusian_1"], 10, 0, [("xp", 600)], big=True),
  Q("combustion", "Combustion Power", ["Burns rocket fuels for huge rotational power. Methane and liquid hydrogen burn best."],
    [I("northstar:combustion_engine")], ["venusian_64"], 12, 0, [("xp", 300)]),
  # Mercury
  Q("mercury", "Closest to the Sun", ["Land on Mercury. No air at all, and harsh sun."],
    [DIM("northstar:mercury")], ["planets_intro"], 2, 3.5, [("xp", 500)]),
  Q("tungsten", "Tungsten", ["Tungsten ore is only found on Mercury. Smelt it and press it into sheets."],
    [I("northstar:raw_tungsten_ore", 16), I("northstar:tungsten_sheet", 8)], ["mercury"], 4, 3.5),
  Q("mercurian_1", "Mercurian Science", ["Sequenced assembly on a tungsten sheet: shelf fungus, mercury stone, 250 mB water, press."],
    [I("kubejs:mercurian_science_pack")], ["tungsten"], 6, 3.5, [("xp", 400)]),
  Q("mercurian_64", "Mercurian Industry", ["Unlocks the Solar Panel."], [I("kubejs:mercurian_science_pack", 64)], ["mercurian_1"], 8, 3.5, [("xp", 600)], big=True),
  Q("solar", "Solar Farm", ["Free power wherever there's sun. Great for stations and outposts."],
    [I("northstar:solar_panel", 4)], ["mercurian_64"], 10, 3.5, [("xp", 300)]),
 ]),

 ("endgame", "6. Warp", "kubejs:warp_drive_core", "The final build", [
  Q("two_worlds", "Interplanetary Supply Chain", [
    "Complete science on &eany two&r planets. Shipping materials between worlds is the real puzzle: dedicated cargo ships, a station hub, or factories on site. Your call."],
    [CHECK], ["martian_64", "venusian_64", "mercurian_64"], 0, 0, [("xp", 500)], min=2),
  Q("warp", "Warp Drive Core", [
    "A 5x5 mechanical crafting recipe: Kinetic and Lunar packs, Earth-branch packs of any kind, packs from two different planets, titanium blocks and a nether star.",
    "Build it, and you've beaten Stellar Foundry. Congratulations, engineer."],
    [I("kubejs:warp_drive_core")], ["two_worlds"], 2, 0, [("xp", 5000)], big=True),
  Q("grand_tour", "Grand Tour", ["Optional: produce science on all three planets."],
    [I("kubejs:martian_science_pack", 16), I("kubejs:venusian_science_pack", 16), I("kubejs:mercurian_science_pack", 16)],
    ["two_worlds"], 2, 2, [("xp", 2000)], optional=True),
 ]),
]


def build(MC, write):
    root = os.path.join(MC, "config", "ftbquests", "quests")
    write(os.path.join(root, "data.snbt"), snbt({
        "version": 13, "default_consume_items": False, "default_autoclaim_rewards": "disabled",
        "default_quest_shape": "circle", "default_quest_disable_jei": False, "disable_gui": False,
        "grid_scale": D(0.5), "title": "Stellar Foundry",
        "icon": {"id": "kubejs:warp_drive_core", "count": 1}, "lock_message": "",
    }) + "\n")
    write(os.path.join(root, "chapter_groups.snbt"), snbt({"chapter_groups": []}) + "\n")

    allkeys = [q[0] for c in CHAPTERS for q in c[4]]
    assert len(allkeys) == len(set(allkeys)), "duplicate quest keys"
    for ci, (ckey, ctitle, cicon, csub, quests) in enumerate(CHAPTERS):
        qlist = []
        for key, title, desc, tasks, deps, x, y, rewards, opts in quests:
            for d in deps:
                assert d in allkeys, (key, d)
            q = {"id": qid("q:" + key), "title": title, "x": D(x * 2), "y": D(y * 2)}
            if desc:
                q["description"] = desc
            if deps:
                q["dependencies"] = [qid("q:" + d) for d in deps]
            if opts.get("min"):
                q["min_required_dependencies"] = opts["min"]
            if opts.get("big"):
                q["size"] = D(1.5); q["shape"] = "gear"
            if opts.get("optional"):
                q["optional"] = True; q["shape"] = "diamond"
            tl = []
            for ti, t in enumerate(tasks):
                tid = qid(f"t:{key}:{ti}")
                if t[0] == "item":
                    tl.append({"id": tid, "type": "item", "item": {"id": t[1], "count": 1}, "count": L(t[2])})
                elif t[0] == "dim":
                    tl.append({"id": tid, "type": "dimension", "dimension": t[1]})
                else:
                    tl.append({"id": tid, "type": "checkmark"})
            q["tasks"] = tl
            rl = []
            for ri, r in enumerate(rewards):
                rid = qid(f"r:{key}:{ri}")
                if r[0] == "xp":
                    rl.append({"id": rid, "type": "xp", "xp": r[1]})
                else:
                    rl.append({"id": rid, "type": "item", "item": {"id": r[1], "count": 1}, "count": r[2]})
            q["rewards"] = rl
            qlist.append(q)
        write(os.path.join(root, "chapters", ckey + ".snbt"), snbt({
            "id": qid("c:" + ckey), "group": "", "order_index": ci, "filename": ckey,
            "title": ctitle, "subtitle": [csub], "icon": {"id": cicon, "count": 1},
            "default_quest_shape": "", "default_hide_dependency_lines": False,
            "quests": qlist, "quest_links": [], "images": [],
        }) + "\n")

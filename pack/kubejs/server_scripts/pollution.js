// Stellar Foundry - Pollution and "biter" attacks (Factorio-style factory pressure)
//
// Furnaces, blaze burners, coke ovens and engines that you place are tracked. Every 30 s, each
// ACTIVE one adds pollution to its 64x64-block region. Pollution slowly decays. When a region near
// a player gets too polluted, hostile mobs come for the factory. Check the local level by
// wearing Engineer's Goggles and sneaking.
//
// Tuning knobs are at the top. Set POL_ENABLED = false to switch the whole mechanic off.

var POL_ENABLED = true
const POL_CYCLE_TICKS = 600          // how often pollution is counted (30 s)
const POL_REGION = 64                // region size in blocks
const POL_DECAY = 0.95               // pollution kept per cycle (5% decays away)
const POL_WARN_AT = 40               // warning message threshold
const POL_ATTACK_AT = 80             // attack threshold
const POL_ATTACK_CHANCE = 0.35       // chance per cycle once above the threshold
const POL_MAX_WAVE = 8
const POL_ATTACK_DIMS = ['minecraft:overworld']
const POL_MOBS = ['minecraft:husk', 'minecraft:spider', 'minecraft:husk', 'minecraft:vindicator']

// block id -> pollution per cycle when active. 'lit' blocks only count while lit.
const POL_POLLUTERS = {
  'minecraft:furnace': 1, 'minecraft:blast_furnace': 2, 'minecraft:smoker': 1,
  'create:blaze_burner': 2,
  'northstar:combustion_engine': 4,
  'tfmg:coke_oven': 3, 'tfmg:firebox': 2, 'tfmg:blast_furnace_output': 4,
  'tfmg:regular_engine': 3, 'tfmg:radial_engine': 4, 'tfmg:large_engine': 6,
  'tfmg:simple_large_engine': 5, 'tfmg:turbine_engine': 6,
  'tfmg:steel_distillation_controller': 3, 'tfmg:pumpjack_base': 2
}

// ---- persistent POL_state: server.persistentData.stellar_pollution = { sources: [...], regions: {...} }
let POL_state = null
let POL_tickCounter = 0
let POL_warned = false

function POL_load(server) {
  if (POL_state) return POL_state
  POL_state = { sources: {}, regions: {} }
  try {
    var raw = server.persistentData.getString('stellar_pollution')
    if (raw && raw.length > 0) POL_state = JSON.parse(raw)
  } catch (e) { console.warn(`Pollution: could not read saved POL_state (${e}), starting fresh`) }
  if (!POL_state.sources) POL_state.sources = {}
  if (!POL_state.regions) POL_state.regions = {}
  return POL_state
}
function POL_save(server) {
  if (POL_state) server.persistentData.putString('stellar_pollution', JSON.stringify(POL_state))
}
function POL_regionKey(dim, x, z) {
  return `${dim}|${Math.floor(x / POL_REGION)}|${Math.floor(z / POL_REGION)}`
}

Object.keys(POL_POLLUTERS).forEach(id => {
  BlockEvents.placed(id, event => {
    if (!POL_ENABLED) return
    var b = event.block
    var s = POL_load(event.server)
    s.sources[`${b.dimension}|${b.x}|${b.y}|${b.z}`] = id
  })
  BlockEvents.broken(id, event => {
    if (!POL_ENABLED) return
    var b = event.block
    var s = POL_load(event.server)
    delete s.sources[`${b.dimension}|${b.x}|${b.y}|${b.z}`]
  })
})

function POL_isActive(block, id) {
  var props = block.properties
  if (id === 'create:blaze_burner') {
    var heat = String(props.get('blaze'))
    return heat === 'kindled' || heat === 'seething' || heat === 'fading'
  }
  if (props.containsKey('lit')) return String(props.get('lit')) === 'true'
  return true // engines etc: counted while their chunk is loaded
}

function POL_surfaceNear(level, x, y, z) {
  for (let dy = 8; dy >= -8; dy--) {
    var yy = y + dy
    var here = level.getBlock(x, yy, z)
    var below = level.getBlock(x, yy - 1, z)
    var above = level.getBlock(x, yy + 1, z)
    if (String(here.id) === 'minecraft:air' && String(above.id) === 'minecraft:air' &&
        String(below.id) !== 'minecraft:air' && String(below.id) !== 'minecraft:water') return yy
  }
  return null
}

function POL_attack(server, player, level, pollution) {
  var n = Math.min(POL_MAX_WAVE, 2 + Math.floor(pollution / 40))
  var spawned = 0
  for (let i = 0; i < n * 3 && spawned < n; i++) {
    var ang = Math.random() * Math.PI * 2
    var dist = 20 + Math.random() * 12
    var x = Math.floor(player.x + Math.cos(ang) * dist)
    var z = Math.floor(player.z + Math.sin(ang) * dist)
    var y = POL_surfaceNear(level, x, Math.floor(player.y), z)
    if (y == null) continue
    var mob = level.createEntity(POL_MOBS[Math.floor(Math.random() * POL_MOBS.length)])
    if (mob == null) continue
    mob.setPosition(x + 0.5, y, z + 0.5)
    mob.spawn()
    spawned++
  }
  if (spawned > 0) {
    player.tell(`\u00a7cYour pollution has drawn an POL_attack! (${spawned} hostiles incoming)`)
    player.runCommandSilent('playsound minecraft:event.raid.horn hostile @s ~ ~ ~ 0.6 1')
  }
  return spawned
}

ServerEvents.tick(event => {
  if (!POL_ENABLED) return
  POL_tickCounter++
  if (POL_tickCounter % POL_CYCLE_TICKS !== 0) return
  var server = event.server
  try {
    var s = POL_load(server)
    // decay
    Object.keys(s.regions).forEach(k => {
      s.regions[k] = s.regions[k] * POL_DECAY
      if (s.regions[k] < 0.5) delete s.regions[k]
    })
    // emit
    Object.keys(s.sources).forEach(key => {
      var parts = key.split('|')
      var dim = parts[0], x = parseInt(parts[1]), y = parseInt(parts[2]), z = parseInt(parts[3])
      var level = server.getLevel(dim)
      if (level == null) return
      if (!level.isLoaded(new BlockPos(x, y, z))) return
      var block = level.getBlock(x, y, z)
      var id = s.sources[key]
      if (String(block.id) !== id) { delete s.sources[key]; return } // removed by machine/explosion
      if (!POL_isActive(block, id)) return
      var rk = POL_regionKey(dim, x, z)
      s.regions[rk] = (s.regions[rk] || 0) + POL_POLLUTERS[id]
    })
    // attacks
    server.players.forEach(player => {
      var dim = String(player.level.dimension)
      if (POL_ATTACK_DIMS.indexOf(dim) < 0) return
      if (player.isCreative() || player.isSpectator()) return
      var rk = POL_regionKey(dim, player.x, player.z)
      var p = s.regions[rk] || 0
      if (p >= POL_ATTACK_AT && Math.random() < POL_ATTACK_CHANCE) {
        if (POL_attack(server, player, player.level, p) > 0) s.regions[rk] = p * 0.6
      } else if (p >= POL_WARN_AT && Math.random() < 0.3) {
        player.setStatusMessage('\u00a76The air smells of smoke. Something out there has noticed your factory.')
      }
    })
    POL_save(server)
  } catch (e) {
    if (!POL_warned) { console.error(`Pollution cycle failed: ${e}`); POL_warned = true }
  }
})

// Wear Engineer's Goggles and sneak to read local pollution
let POL_gogglesTick = 0
ServerEvents.tick(event => {
  if (!POL_ENABLED) return
  POL_gogglesTick++
  if (POL_gogglesTick % 20 !== 0) return
  try {
    var s = POL_load(event.server)
    event.server.players.forEach(player => {
      if (!player.isCrouching()) return
      if (String(player.headArmorItem.getIdLocation()) !== 'create:goggles') return
      var p = Math.round(s.regions[POL_regionKey(String(player.level.dimension), player.x, player.z)] || 0)
      var colour = p >= POL_ATTACK_AT ? '\u00a7c' : (p >= POL_WARN_AT ? '\u00a76' : '\u00a7a')
      player.setStatusMessage(`${colour}Local pollution: ${p}  (warning ${POL_WARN_AT}, attacks from ${POL_ATTACK_AT})`)
    })
  } catch (e) {
    if (!POL_warned) { console.error(`Pollution goggles readout failed: ${e}`); POL_warned = true }
  }
})

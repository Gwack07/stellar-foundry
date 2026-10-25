// Stellar Foundry - Planet weather
//
// Mars: dust storms roll in for ~2 of every 12 minutes. Out in the open you're slowed and
//       your vision darkens. Get under a roof.
// Venus: acid rain for ~3 of every 10 minutes. Exposed to the sky, it poisons you
//        (poison can't kill, but it will make a mess of your health bar).
// Shelter = any block above you (canSeeSky is false). Sitting in a seat (ship/rocket) also counts.

var WX_ENABLED = true
const WX_CHECK_TICKS = 40
const WX_WEATHER = {
  'northstar:mars': {
    period: 12 * 1200, length: 2 * 1200,
    start: '§6A dust storm is rolling in. Find shelter!',
    during: '§6Dust storm - take shelter',
    end: '§eThe dust storm has passed.',
    effects: [['minecraft:slowness', 60, 0], ['minecraft:darkness', 60, 0]]
  },
  'northstar:venus': {
    period: 10 * 1200, length: 3 * 1200,
    start: '§aThe clouds are thickening. Acid rain incoming!',
    during: '§aAcid rain - get under cover',
    end: '§2The acid rain has eased.',
    effects: [['minecraft:poison', 60, 0]]
  }
}

var WX_tick = 0
const WX_lastState = {}
let WX_warned = false

ServerEvents.tick(event => {
  if (!WX_ENABLED) return
  WX_tick++
  if (WX_tick % WX_CHECK_TICKS !== 0) return
  try {
    event.server.players.forEach(player => {
      var dim = String(player.level.dimension)
      var w = WX_WEATHER[dim]
      if (!w) return
      var phase = player.level.getTime() % w.period
      var active = phase < w.length
      var key = String(player.username) + dim
      if (WX_lastState[key] !== active) {
        if (WX_lastState[key] !== undefined) player.tell(active ? w.start : w.end)
        WX_lastState[key] = active
      }
      if (!active || player.isCreative() || player.isSpectator()) return
      if (player.isPassenger()) return
      if (!player.block.getCanSeeSky()) return
      w.effects.forEach(e => player.potionEffects.add(e[0], e[1], e[2], false, false))
      player.setStatusMessage(w.during)
    })
  } catch (e) {
    if (!WX_warned) { console.error(`Planet weather failed: ${e}`); WX_warned = true }
  }
})

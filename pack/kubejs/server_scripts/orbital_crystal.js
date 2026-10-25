// Stellar Foundry - Orbital Crystallisation
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

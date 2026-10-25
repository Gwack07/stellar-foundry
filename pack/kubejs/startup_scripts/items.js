// Stellar Foundry - custom items
// Science packs are research currency: they go into the machines that unlock the next step.

const SCIENCE_PACKS = [
  'kinetic',
  'logistic',
  'chemical',
  'aeronautical',
  'industrial',
  'lunar',
  'martian',
  'venusian',
  'mercurian'
]

StartupEvents.registry('item', event => {
  SCIENCE_PACKS.forEach(key => {
    event.create(`${key}_science_pack`).maxStackSize(64).rarity('uncommon')
    event.create(`incomplete_${key}_science_pack`).maxStackSize(1) // sequenced assembly
  })
  event.create('vacuum_crystal').maxStackSize(64).rarity('rare')
  event.create('warp_drive_core').maxStackSize(1).rarity('epic').fireResistant()
})

// Transitional "incomplete" packs only exist mid-assembly: keep them out of the creative tab
StartupEvents.modifyCreativeTab('kubejs:tab', event => {
  SCIENCE_PACKS.forEach(key => event.remove(`kubejs:incomplete_${key}_science_pack`))
})

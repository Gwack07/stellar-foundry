// Stellar Foundry - tooltips and recipe-viewer notes

ItemEvents.modifyTooltips(event => {
  event.add('kubejs:kinetic_science_pack', ['\u00a77Earth - Create machinery'])
  event.add('kubejs:logistic_science_pack', ['\u00a77Earth branch - brass and logistics'])
  event.add('kubejs:chemical_science_pack', ['\u00a77Earth branch - titanium chemistry'])
  event.add('kubejs:aeronautical_science_pack', ['\u00a77Earth branch - flight'])
  event.add('kubejs:industrial_science_pack', ['\u00a77Earth branch - oil, steel and plastics'])
  event.add('kubejs:lunar_science_pack', ['\u00a77The Moon'])
  event.add('kubejs:martian_science_pack', ['\u00a77Planet - Mars'])
  event.add('kubejs:venusian_science_pack', ['\u00a77Planet - Venus'])
  event.add('kubejs:mercurian_science_pack', ['\u00a77Planet - Mercury'])
  event.add('kubejs:vacuum_crystal', ['\u00a7dGrown in Earth orbit from polished rose quartz'])
  event.add('kubejs:warp_drive_core', ['\u00a76The way home... or further out.'])
})

// Hide mid-assembly transitional items from the JEI item list (they still show inside recipes)
RecipeViewerEvents.removeEntries('item', event => {
  event.remove('kubejs:incomplete_kinetic_science_pack')
  event.remove('kubejs:incomplete_logistic_science_pack')
  event.remove('kubejs:incomplete_chemical_science_pack')
  event.remove('kubejs:incomplete_aeronautical_science_pack')
  event.remove('kubejs:incomplete_industrial_science_pack')
  event.remove('kubejs:incomplete_lunar_science_pack')
  event.remove('kubejs:incomplete_martian_science_pack')
  event.remove('kubejs:incomplete_venusian_science_pack')
  event.remove('kubejs:incomplete_mercurian_science_pack')
})

RecipeViewerEvents.addInformation('item', event => {
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
})

// Stellar Foundry - remove the original recipes of gated machines.
// Their science-pack versions live in kubejs/data/stellar/recipe/gated (namespace 'stellar',
// so the mod filter below never removes them).

ServerEvents.recipes(event => {
  event.remove({ output: 'create:empty_blaze_burner', mod: 'create' })
  event.remove({ output: 'ae2:controller', mod: 'ae2' })
  event.remove({ output: 'northstar:astronomy_table', mod: 'northstar' })
  event.remove({ output: 'northstar:interplanetary_navigator', mod: 'northstar' })
  event.remove({ output: 'northstar:electrolysis_machine', mod: 'northstar' })
  event.remove({ output: 'northstar:combustion_engine', mod: 'northstar' })
  event.remove({ output: 'northstar:solar_panel', mod: 'northstar' })
})

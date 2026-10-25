// Stellar Foundry - starter kit and welcome (once per player)

PlayerEvents.loggedIn(event => {
  var player = event.player
  var data = player.persistentData
  if (data.getBoolean('stellar_kit')) return
  data.putBoolean('stellar_kit', true)

  player.give(Item.of('ftbquests:book'))
  player.give(Item.of('create:wrench'))
  player.give(Item.of('create:goggles'))
  player.give(Item.of('minecraft:bread', 16))

  player.tell('§6§lWelcome to Stellar Foundry!')
  player.tell('§7Open the §equest book§7 to start. Your goal: the Warp Drive Core.')
  player.tell('§7Watch your pollution: wear Engineer\'s Goggles and sneak to check it.')
})

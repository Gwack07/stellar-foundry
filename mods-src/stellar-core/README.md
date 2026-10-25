# Stellar Foundry Core (stellarcore)

Our own NeoForge 1.21.1 mod, from the official MDK. CI (`.github/workflows/java-mod.yml`) builds it
and uploads the jar as an artifact. It is **not** in the pack yet: add it to `pack/mods` once it has
features (publish the jar to a GitHub release and reference that URL + sha512).

To depend on Create, add the Create maven (`https://maven.createmod.net`) and
`compileOnly "com.simibubi.create:create-1.21.1:6.0.10-280:slim"` (plus Ponder/Flywheel/Registrate
as Create's README describes), and a `[[dependencies.stellarcore]] modId="create"` entry.

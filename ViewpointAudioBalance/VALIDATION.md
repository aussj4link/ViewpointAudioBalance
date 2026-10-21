# Validation record

2026-10-21, version 0.1.0 Workshop candidate.

Inspected the provided engine and Viewpoint class signatures/bytecode for clip volume calculation, menu-volume separation, Ambient routing, player access, the public 3D mode flag and legacy annotation descriptors. Inspected the user's log for the installed ZombieBuddy version (2.3.4) and prior distance-mod definition results.

The distributed experimental JAR was compiled with JDK 17 against minimal, locally generated signature stand-ins because the workspace lacks JDK 25 and the actual agent JAR. Only original production classes are packaged. This is a compile/signature check, not a build against the complete actual runtime. The source includes a real-dependency build command for JDK 25.

Portable Java checks passed: independent effects/ambient gain; first/third-person modes; isometric and no-player bypass; UI/Music priority; unknown categories; zero-volume preservation; repeated calls without accumulated gain; recognized world categories; group mutes; disabled state; finite bounds; non-finite configuration fallback; overflow bypass; and patch metadata. Repeated calls account for many of the checks; their count is not a measure of integration coverage.

Lua syntax and options lifecycle/configuration checks are run with Lua 5.4 and API stand-ins. They do not establish Kahlua bridge or native options-screen behavior. Archive checks verify only the intended production classes are in the JAR and no dependency classes or assets are bundled.

## Initial in-game result

The project owner's console(6).txt confirms production Java loading, discovery of Patch_EffectiveVolume, Lua exposure of Settings as ViewpointAudioBalance, the native volume patch and options-page registration. Settings progressed from 2x/2x to 6x/2x and 6x/6x. No VAB exception, missing-bridge warning or failed patch appears in that log. Other game/mod warnings exist; this is not a clean bill of health for the whole installation.

The owner reports that audio is now clearly audible in first and third person, gain choices were tested and the live on/off control worked. 6x was their preferred level. They noticed no errors or conflicts with their active mods. This is one user's listening report, not a calibrated measurement or blanket compatibility result.

Remaining explicit checks: isometric restoration with active loops, music/UI exclusion in-game, restart/save persistence, directional/muffled audio comparisons and broader performance/mod compatibility. These were not individually confirmed in the latest report. Follow TESTING.md.

## Candidate packaging

The Workshop candidate keeps the exact tested Java binary (SHA-256 `d59451a80aa2ab6d8c096491bb17aa8ddfe6e7a42b6c99d7b67b3ee67e36a3ae`). Its internal experimental diagnostic label remains unchanged. The visible mod/page name and documentation are polished; no gain algorithm, defaults, category routing, mod ID or preference key changes were made. Lua options checks were repeated after the display-name edit. Nothing was published to Steam.

# Viewpoint - Audio Balance

Independent volume controls for world effects and background ambience in Project Viewpoint's first- and third-person modes.

If footsteps, doors, combat or the ambient soundscape feel too quiet in Viewpoint, this mod lets you raise them to a comfortable level without turning up music or menu clicks. It adjusts playback gain while retaining the game's sound events, spatial positioning and distance settings.

**Version 0.1.0 — initial Steam Workshop release.** All 12 manual Workshop regression checks were reported as passing in Project Zomboid Build 42.21. This validates the tested configuration, not compatibility with every mod or future build.

[Steam Workshop page](https://steamcommunity.com/sharedfiles/filedetails/?id=3823974655) | [Testing and validation](TESTING.md) | [Detailed validation notes](VALIDATION.md)

## Installation

### Steam Workshop (recommended)

1. Subscribe to [Viewpoint - Audio Balance](https://steamcommunity.com/sharedfiles/filedetails/?id=3823974655) and its required items, **Project Viewpoint** and **ZombieBuddy**.
2. Fully close and restart Project Zomboid after installation so the Java component can load.
3. Enable **Viewpoint - Audio Balance** for the save you want to use.
4. Open **Options → Mods → Viewpoint - Audio Balance** and adjust the two gain controls.

### Manual installation (alternative)

1. Fully close Project Zomboid.
2. Extract `ViewpointAudioBalance` into `%USERPROFILE%\Zomboid\mods\`.
3. Confirm `%USERPROFILE%\Zomboid\mods\ViewpointAudioBalance\42\mod.info` exists.
4. Enable the mod for your save and fully restart the game.
5. Open **Options → Mods → Viewpoint - Audio Balance** to configure it.

The compiled JAR is included. Keep your existing Viewpoint/ZombieBuddy installation; no compiler or manual game-file edits are needed to play. Avoid keeping both a local development copy and a Workshop copy enabled at the same time. See WORKSHOP_SETUP.md for upload preparation.

## Controls

| Control | Coverage |
| --- | --- |
| World effects gain | Footsteps, doors, combat, zombie voices, item/animal/vehicle effects and other recognized world effects |
| Background ambience gain | The game's Ambient group: combined day/night/weather soundscape and environmental hums |
| Enable Viewpoint audio balance | Turns gain adjustment on or off without reloading |

Each group starts at **2x** and offers mute, 0.5x, 1x, 1.5x, 2x, 3x, 4x, 6x, 8x, 12x and 16x. **1x means unchanged.** Apply changes while playing. Start at a lower output volume when trying amplification and increase gradually; high gain can distort sounds that are already loud.

Effects and ambience are independent, not multiplied together. Night sounds and weather may be layers of one FMOD event, so they share the ambience control. Some individual wildlife/meta events follow the effects group instead.

This mod's gain bypasses isometric mode, UI categories and music. Native volume preferences are never rewritten, and existing native mute/volume controls still apply. Settings save locally through the game's built-in Mod Options system; no separate settings mod is required.

Installing, updating or removing the Java mod requires a **full game restart**. The in-game enable checkbox bypasses the effect immediately; it is different from unloading the hook.

## Requirements and compatibility

- Project Zomboid **Build 42.21**.
- **Project Viewpoint**, tested against the supplied **0.1.6.1 API**.
- **ZombieBuddy**, tested in-game with **2.3.4**. The package allows 2.3.0–2.3.4; newer agent APIs need verification/rebuilding before expanding the version limit.

There is one small hook at an existing clip-volume calculation, with no extra update loop, replacement audio bank or save-data changes. Mods patching that same calculation or redefining categories may interact. Unsupported custom categories and sounds bypassing GameSoundClip may not respond.

**Spatial Zombie Audio is optional and separate.** Keep it enabled if you want its zombie voice-distance overrides. This package adjusts volume only and contains no distance overrides. Its isometric gain bypass does not remove changes made by another mod.

## Troubleshooting

Look for `[VAB]` entries in `%USERPROFILE%\Zomboid\console.txt`: Java loading, native options registration and selected-gain messages. The tested JAR retains its original `Experimental 0.1.0` diagnostic label; the Workshop release uses that tested binary.

If controls appear but do nothing, check Java-mod loading and the installed agent version, then fully restart. If only particular sounds fail to respond, report their names/context and camera mode.

Report bugs through the Steam Workshop comments or GitHub. Include your game, Viewpoint and ZombieBuddy versions, active mods, both gain values and relevant `console.txt` messages. Source and build instructions are included.

## Credits and license

Development assistance: **ChatGPT (OpenAI)**. Thanks to the creators of Project Viewpoint and ZombieBuddy. This is an independent addon, not an official release from those projects.

Original code and documentation are available under the included MIT license. Third-party game, Viewpoint and ZombieBuddy binaries/assets are not bundled or relicensed.

# Architecture and findings

## Evidence

The supplied console log shows Spatial Zombie Audio loading all ten expected event mappings with explicit 2/35 distance values on three starts. Its diagnostic did not report a failure in those entries. The user's observed distance improvement is useful listening evidence, but the log does not establish the attenuation curve, calibrated loudness or a root cause for the quiet world mix.

In the supplied 42.21 engine:

- `GameSoundClip.getEffectiveVolume()` returns clip volume times the user's per-sound volume. Both native emitter playback and ambient playback paths consult it.
- `GameSoundClip.getEffectiveVolumeInMenu()` is a separate method and is not patched.
- `SoundManager.setAmbientVolume(float)` overwrites its input with 1 and sets the ambience VCA to that value. `getAmbientVolume()` also returns 1. Simply calling this setter from Lua would not supply an independent gain control in this build.
- Generated sound definitions assign `WorldAmbiance`, tree/tent/vehicle ambience and various environmental hums to `GameSound.MasterVolume.Ambient`. The combined WorldAmbiance event includes day/night/weather parameters, so a single event's constituent layers cannot be split by this clip-level gain.
- World effects use the categories Animals, Item, Meta, Object, Player, Vehicle, World and Zombie. Music/UI have separate categories; Music also has an explicit master route.

The supplied Viewpoint's `viewpoint.core.View.enabled` is a public volatile boolean, true for its first/third-person 3D rendering. Its thirdPerson flag selects the perspective within 3D. This companion reads the enabled field directly; it does not patch Viewpoint or infer mode from key presses. A missing API fails to unchanged gain and logs once.

## Implementation

One ZombieBuddy exit advice hooks `zombie.audio.GameSoundClip.getEffectiveVolume`. It passes the original result and clip to `Mix.adjust` and writes the result back. The legacy Patch annotations match those observed in the supplied Viewpoint JAR for the user's ZombieBuddy 2.3.4 installation.

`Mix.adjust` reads an immutable settings snapshot. Disabled settings, no local player, isometric mode, missing API, null data, zero/non-finite input, UI/Music and unsupported categories bypass the gain. Music/UI exclusion takes priority even when a sound has another route. Ambient routing selects only the ambience gain; recognized world categories select only effects gain. No gain accumulates in clip.volume or persisted preferences. Output overflow falls back to the original value.

This hook can run at the game's existing per-sound volume evaluations. It adds constant-time checks and no new sound scan, collection building, native event or update loop. It preserves native event references, positions, min/max distance, occlusion parameters, hearing traits and mix calculations before this final multiplicative adjustment. A louder signal can naturally remain perceptible farther away; preserving the attenuation curve does not guarantee an identical perceived audible radius.

`Settings` is annotated with ZombieBuddy's LuaClass exposure API, named `ViewpointAudioBalance`. Lua calls its static configure method when saved preferences load or the options page is applied. The Java snapshot initially bypasses gain until configured. The Lua page uses native PZAPI.ModOptions comboboxes and a checkbox; no frame polling and no optional external settings mod.

## Limits and tests

Existing bank routing or later processing can affect final loudness. Sounds that avoid GameSoundClip or use unsupported categories may not respond. A mislabeled third-party UI sound in a world category can be boosted. Agent loading, patch application, Lua exposure and initial listening have now been verified in the owner's setup. Formal mode/loop restoration, split-screen, detailed panning/muffling and broader mod compatibility remain outside that evidence. See TESTING.md and VALIDATION.md.

## References

- User-supplied engine JAR, Viewpoint JAR, generated sound definitions and console(5).txt; inspection only, not redistributed.
- https://github.com/zed-0xff/ZombieBuddy/blob/master/doc/ModdingGuide.md — native mod loading, advice and LuaClass exposure. The current guide also covers newer agent APIs; this experimental binary targets the observed legacy 2.3.x signatures.
- https://projectzomboid.com/modding/zombie/audio/GameSoundClip.html

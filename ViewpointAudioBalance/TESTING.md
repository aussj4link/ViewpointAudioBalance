# Listening and integration test

Use a disposable save. Lower Windows/headphone output before testing the new gain. Keep music at your preferred setting; this companion should not affect it. Record both gain choices and the camera mode with each observation.

1. Fully restart with this companion enabled. Check for `[VAB]` loading, page registration and selected-gain messages. Confirm a ZombieBuddy patch message for `GameSoundClip.getEffectiveVolume` and no patch/exposure error.
2. In Options → Mods → Viewpoint - Audio Balance, choose 1x for both and Apply. Compare with the companion's Enable checkbox off; it should sound the same.
3. In first person, set effects to 2x, ambience to 1x. Test footsteps, a door and combat, then zombie voices. Raise effects to 4x or 6x if still too quiet. Observe actual output; linear amplitude multipliers do not translate directly to perceived loudness multipliers.
4. Set effects to 1x and change ambience between 0, 1x and 2x while stationary outside at night. The combined ambient bed should respond independently. Keep the test's weather consistent. A separate owl/meta event may follow world-effects routing rather than the combined bed.
5. Try third person, then isometric. Isometric should return to the original mix despite the selected boosts. Repeat first → third → iso → first with an already-playing ambient loop.
6. Check UI clicks, music and sound previews. They should not follow these gains. If they do, identify the sound and other active mods.
7. Turn the camera with a zombie to one side; check panning. Step into a building and out again to check muffling. Recheck close/distant groans with the original distance mod if you use it.
8. Apply a lower or muted native Sound Volume setting, then restore it. The companion should respect the native mute and multiply the new baseline.
9. Reload the save and fully restart to check persistence. To remove the Java hook, disable this companion and fully restart; a save reload alone does not unload an instrumented method. The original Spatial Zombie Audio mod remains separate.

Send console.txt and report: camera mode; effects/ambience choices; exact sounds that respond or do not; any distortion; and whether isometric, menus/music or directional/muffled audio changed. The code's mode/category tests are not a substitute for these in-game comparisons.

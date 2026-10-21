# Workshop listing and upload notes

**Title:** Viewpoint - Audio Balance

**Version:** 0.1.0 (first Workshop candidate)

**Short summary:** Independent world-effects and ambience volume controls for Project Viewpoint's first- and third-person modes.

Paste the complete BBCode from WORKSHOP_DESCRIPTION.txt into the description. Suggested tags, where offered: **Build 42**, **Audio**, **Interface**. The mod ID remains `ViewpointAudioBalance`; the cosmetic rename does not create a new mod or discard saved preferences.

## Upload preparation

1. Use Project Zomboid's Workshop upload interface to create an item/project folder. Nothing has been uploaded or published by this preparation.
2. In that project's `Contents/mods/` folder, place the included `ViewpointAudioBalance` folder. Confirm the final relative path is `Contents/mods/ViewpointAudioBalance/42/mod.info`.
3. Keep the client JAR, Lua file, common directory, source, license and documentation together. Do not include the test game, console logs or dependency JARs.
4. Add an original preview image or appropriate in-game screenshot through the uploader. This archive has no preview image; the supplied Steam search screenshot is not used as public artwork.
5. Set the title/description, review the item privately, and publish when satisfied. Add Project Viewpoint and ZombieBuddy as required items on the Workshop item page. Required-item links are a separate listing setting from mod.info dependencies.

Required item references:

- Project Viewpoint: https://steamcommunity.com/sharedfiles/filedetails/?id=3809306528
- ZombieBuddy: https://steamcommunity.com/sharedfiles/filedetails/?id=3619862853

The Java agent installation remains a ZombieBuddy setup requirement; subscribing alone is not a substitute for that project's installation procedure.

## Credits

Suggested line: **Development assistance: ChatGPT (OpenAI).** This credits the assistance without implying endorsement by OpenAI or the Viewpoint/ZombieBuddy authors. You remain the publisher and maintainer of your item.

## Validation scope

The owner's initial in-game test was successful in first and third person, with working gain choices and no noticed conflicts in that setup. The console confirms Java loading, Lua exposure, patch application and settings changes. See VALIDATION.md for the evidence and remaining checks. No broad multi-mod compatibility guarantee is made.

Complete the remaining mode/loop restoration, music/UI exclusion, reload/persistence and panning/muffling checks in TESTING.md before calling it a finished stable release. The candidate keeps the tested audio binary, gain defaults, mod ID and preference keys intact.

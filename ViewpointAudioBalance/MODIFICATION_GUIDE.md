# Modification guide

Safe editorial changes: names, descriptions, explanatory text and log wording, while preserving accurate experimental status and mod identity.

Changes requiring tests: default gain choices, allowed bounds, effects category allowlist, Ambient-group classification, options installation/load timing and game/Viewpoint/agent version ranges. For example, changing the default from 2x to 3x requires updating the Lua selected item, README and listening tests. Keep the gain list and Java 0..16 bound consistent.

High-risk changes: patch targets, annotation API versions, Viewpoint mode detection, shared audio/VCA routing, menu/music exclusion and any FMOD, listener, event-position or attenuation change. Do not broaden the hook to menu effective volume or multiply global SFX volume as a shortcut; that would change the scope of UI and other audio.

To support an additional custom effects category, verify its actual sounds first, add its exact name to Mix.EFFECT_CATEGORIES, then test with the owning mod. Ambient routing is classified by MasterVolume.Ambient, not by a substring such as 'night' in a sound name. Splitting layers within WorldAmbiance requires a different FMOD-aware design.

To disable balance for diagnosis, use the checkbox or 1x choices. Removing the Lua file leaves initial Java defaults at unity after a full restart, but does not uninstall the instrumented method. Do not redistribute compilation stand-ins as runtime game or framework classes.

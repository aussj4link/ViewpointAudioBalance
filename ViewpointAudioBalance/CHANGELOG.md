# Changelog

## 0.1.0 — first Workshop candidate, 2026-10-21

- Chosen public name: **Viewpoint - Audio Balance**.
- Confirmed Java loading, patch application, Lua exposure and options registration in the owner's game log.
- Owner reported successful first-/third-person gain testing, useful 6x levels and working live enable/disable.
- Polished display names, documentation and Steam-ready BBCode description.
- Kept the tested audio JAR, gain defaults, mod ID and option keys unchanged.

### Initial implementation

- Added a Viewpoint-only playback gain hook with separate effects and Ambient-group multipliers.
- Added native local Mod Options controls, defaults 2x/2x, range muted through 16x.
- Added explicit isometric, no-player, Music and UI bypasses.
- Added source, rebuild instructions, logic tests and an in-game listening matrix.
- Kept Spatial Zombie Audio as a separate optional companion; no distance settings are included here.
- Initial agent integration and audibility have now been tested by the owner; remaining checks are recorded in VALIDATION.md.

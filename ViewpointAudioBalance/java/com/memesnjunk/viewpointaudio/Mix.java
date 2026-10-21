package com.memesnjunk.viewpointaudio;

import java.util.Set;
import viewpoint.core.View;
import zombie.audio.GameSound;
import zombie.audio.GameSoundClip;
import zombie.characters.IsoPlayer;

/** Category-based playback gain. No event, clip or listener state is mutated. */
public final class Mix {
    private static final Set<String> EFFECT_CATEGORIES = Set.of(
            "Animals", "Item", "Meta", "Object", "Player", "Vehicle", "World", "Zombie");
    private static volatile boolean missingModeReported;

    private Mix() { }

    /**
     * Receives the original effective clip volume and the clip being evaluated.
     * Returns that volume times exactly one selected gain, or the input on bypass.
     * Reading View.enabled at the playback boundary makes camera changes immediate
     * at the next native volume evaluation; no Lua polling/frame handler is needed.
     * Only existing Ambient routing and known world categories are covered. Sounds
     * that bypass GameSoundClip, or unsupported custom categories, are not captured.
     */
    public static float adjust(float original, GameSoundClip clip) {
        Settings.Config config = Settings.current;
        if (!config.enabled() || clip == null || !Float.isFinite(original) || original <= 0.0f) {
            return original;
        }
        try {
            if (!View.enabled || IsoPlayer.getInstance() == null) return original;
        } catch (LinkageError unavailable) {
            if (!missingModeReported) {
                missingModeReported = true;
                System.out.println("[VAB] Viewpoint mode API unavailable; gain bypassed: "
                        + unavailable.getClass().getSimpleName());
            }
            return original;
        }
        GameSound sound = clip.gameSound;
        if (sound == null) return original;
        String category = sound.getCategory();
        if (sound.master == GameSound.MasterVolume.Music
                || "Music".equals(category) || "UI".equals(category)) return original;

        float gain;
        if (sound.master == GameSound.MasterVolume.Ambient) {
            gain = config.ambience();
        } else if (category != null && EFFECT_CATEGORIES.contains(category)) {
            gain = config.effects();
        } else {
            return original;
        }
        float adjusted = original * gain;
        return Float.isFinite(adjusted) ? adjusted : original;
    }
}

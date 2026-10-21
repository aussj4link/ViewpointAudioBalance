package com.memesnjunk.viewpointaudio;

import me.zed_0xff.zombie_buddy.Exposer;

/** A small Lua-facing settings bridge, registered by ZombieBuddy on Lua setup. */
@Exposer.LuaClass(name = "ViewpointAudioBalance")
public final class Settings {
    // One immutable snapshot keeps an audio read consistent with a settings update.
    static volatile Config current = new Config(false, 1.0f, 1.0f);

    record Config(boolean enabled, float effects, float ambience) { }

    private Settings() { }

    /**
     * Inputs are local option values, in linear gain (1 = unchanged).
     * Publishes a validated snapshot; never changes game volume preferences.
     * Non-finite gains fall back to unity, and finite gains are bounded 0..16.
     */
    public static void configure(boolean enabled, double effects, double ambience) {
        Config next = new Config(enabled, validGain(effects), validGain(ambience));
        if (!next.equals(current)) {
            current = next;
            System.out.println("[VAB] enabled=" + enabled + " effects=" + next.effects()
                    + "x ambience=" + next.ambience()
                    + "x; applies only in Viewpoint 3D with a local player.");
        }
    }

    public static String version() { return "0.1.0-experimental"; }

    private static float validGain(double value) {
        if (!Double.isFinite(value)) return 1.0f;
        return (float) Math.max(0.0, Math.min(16.0, value));
    }
}

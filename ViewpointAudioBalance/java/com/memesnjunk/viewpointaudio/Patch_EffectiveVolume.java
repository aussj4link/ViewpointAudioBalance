package com.memesnjunk.viewpointaudio;

import me.zed_0xff.zombie_buddy.Patch;
import zombie.audio.GameSoundClip;

/** Adjusts the native runtime value, preserving the game's own volume calculation. */
@Patch(className = "zombie.audio.GameSoundClip", methodName = "getEffectiveVolume")
public final class Patch_EffectiveVolume {
    private Patch_EffectiveVolume() { }

    @Patch.OnExit
    public static void exit(@Patch.This GameSoundClip clip,
                            @Patch.Return(readOnly = false) float volume) {
        // ZombieBuddy inlines this advice and writes the parameter back to return.
        volume = Mix.adjust(volume, clip);
    }
}

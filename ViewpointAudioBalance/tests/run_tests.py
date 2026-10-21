#!/usr/bin/env python3
"""Local logic tests with minimal API stand-ins, not a game/agent integration test.

An optional --emit-jar path packages only the tested production classes. This
allows building the experimental binary where only JDK 17 is available. Field
and method signatures used by those classes were checked against supplied APIs.
For a release build, use ../build.py with actual dependencies and JDK 25.
"""
import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

STUBS = {
    "me/zed_0xff/zombie_buddy/Patch.java": '''package me.zed_0xff.zombie_buddy;
import java.lang.annotation.*;
@Retention(RetentionPolicy.RUNTIME) @Target(ElementType.TYPE)
public @interface Patch {
 String className(); String methodName();
 @Retention(RetentionPolicy.RUNTIME) @Target(ElementType.METHOD)
 public @interface OnExit { }
 @Retention(RetentionPolicy.RUNTIME) @Target(ElementType.PARAMETER)
 public @interface This { }
 @Retention(RetentionPolicy.RUNTIME) @Target(ElementType.PARAMETER)
 public @interface Return { boolean readOnly() default true; }
}''',
    "me/zed_0xff/zombie_buddy/Exposer.java": '''package me.zed_0xff.zombie_buddy;
import java.lang.annotation.*;
public class Exposer {
 @Retention(RetentionPolicy.RUNTIME) @Target(ElementType.TYPE)
 public @interface LuaClass { String name() default ""; }
}''',
    "viewpoint/core/View.java": '''package viewpoint.core;
public final class View { public static volatile boolean enabled, thirdPerson; }''',
    "zombie/characters/IsoPlayer.java": '''package zombie.characters;
public class IsoPlayer {
 public static IsoPlayer instance;
 public static IsoPlayer getInstance() { return instance; }
}''',
    "zombie/audio/GameSound.java": '''package zombie.audio;
public class GameSound {
 public enum MasterVolume { Primary, Ambient, Music, VehicleEngine }
 public MasterVolume master = MasterVolume.Primary;
 public String category;
 public String getCategory() { return category; }
}''',
    "zombie/audio/GameSoundClip.java": '''package zombie.audio;
public class GameSoundClip {
 public final GameSound gameSound;
 public GameSoundClip(GameSound sound) { gameSound = sound; }
}''',
}

HARNESS = '''import com.memesnjunk.viewpointaudio.*;
import zombie.audio.*;
import zombie.characters.IsoPlayer;
import viewpoint.core.View;
import me.zed_0xff.zombie_buddy.Patch;
import java.lang.reflect.Method;

public class MixTests {
 private static int checks;
 static void same(float expected, float actual, String name) {
  checks++;
  if (Float.compare(expected, actual) != 0)
   throw new AssertionError(name + ": expected " + expected + ", got " + actual);
 }
 static GameSoundClip clip(String category, GameSound.MasterVolume master) {
  GameSound sound = new GameSound(); sound.category = category; sound.master = master;
  return new GameSoundClip(sound);
 }
 public static void main(String[] args) throws Exception {
  GameSoundClip fx = clip("Zombie", GameSound.MasterVolume.Primary);
  GameSoundClip ambient = clip("World", GameSound.MasterVolume.Ambient);
  IsoPlayer.instance = new IsoPlayer(); View.enabled = true;
  Settings.configure(true, 4, 2);
  same(2f, Mix.adjust(0.5f, fx), "effects gain");
  same(1f, Mix.adjust(0.5f, ambient), "independent ambient gain");
  View.thirdPerson = true;
  same(2f, Mix.adjust(0.5f, fx), "third person");
  View.enabled = false;
  same(0.5f, Mix.adjust(0.5f, fx), "isometric bypass");
  same(0.5f, Mix.adjust(0.5f, ambient), "isometric ambient bypass");
  View.enabled = true; IsoPlayer.instance = null;
  same(0.5f, Mix.adjust(0.5f, fx), "no local player/menu bypass");
  IsoPlayer.instance = new IsoPlayer();
  same(0.5f, Mix.adjust(0.5f, clip("UI", GameSound.MasterVolume.Primary)), "UI unchanged");
  same(0.5f, Mix.adjust(0.5f, clip("Music", GameSound.MasterVolume.Primary)), "music category unchanged");
  same(0.5f, Mix.adjust(0.5f, clip("World", GameSound.MasterVolume.Music)), "music routing unchanged");
  same(0.5f, Mix.adjust(0.5f, clip("UI", GameSound.MasterVolume.Ambient)), "UI takes priority");
  same(0.5f, Mix.adjust(0.5f, clip("CustomUnknown", GameSound.MasterVolume.Primary)), "unknown category bypass");
  same(1f, Mix.adjust(0.5f, clip("CustomUnknown", GameSound.MasterVolume.Ambient)), "ambient route recognition");
  same(0f, Mix.adjust(0f, fx), "existing mute preserved");
  same(0.5f, Mix.adjust(0.5f, null), "null clip bypass");
  same(0.5f, Mix.adjust(0.5f, new GameSoundClip(null)), "null sound bypass");
  for (int i = 0; i < 100; i++) same(2f, Mix.adjust(0.5f, fx), "no accumulated gain");
  for (String category : new String[]{"Animals","Item","Meta","Object","Player","Vehicle","World","Zombie"})
   same(2f, Mix.adjust(0.5f, clip(category, GameSound.MasterVolume.Primary)), "coverage " + category);
  Settings.configure(true, 0, 3);
  same(0f, Mix.adjust(0.5f, fx), "effects mute");
  same(1.5f, Mix.adjust(0.5f, ambient), "effects mute leaves ambient independent");
  Settings.configure(true, 3, 0);
  same(0f, Mix.adjust(0.5f, ambient), "ambient mute");
  same(1.5f, Mix.adjust(0.5f, fx), "ambient mute leaves effects independent");
  Settings.configure(false, 16, 16);
  same(0.5f, Mix.adjust(0.5f, fx), "disabled bypass");
  Settings.configure(true, 999, -1);
  same(8f, Mix.adjust(0.5f, fx), "upper gain bound");
  same(0f, Mix.adjust(0.5f, ambient), "lower gain bound");
  Settings.configure(true, Double.NaN, Double.POSITIVE_INFINITY);
  same(0.5f, Mix.adjust(0.5f, fx), "NaN setting fallback");
  same(0.5f, Mix.adjust(0.5f, ambient), "infinite setting fallback");
  Settings.configure(true, 16, 1);
  same(Float.MAX_VALUE, Mix.adjust(Float.MAX_VALUE, fx), "overflow bypass");
  Method method = Patch_EffectiveVolume.class.getMethod("exit", GameSoundClip.class, float.class);
  if (!method.getParameters()[1].getAnnotation(Patch.Return.class).readOnly()
      && Patch_EffectiveVolume.class.getAnnotation(Patch.class).methodName().equals("getEffectiveVolume")) checks++;
  else throw new AssertionError("Patch annotation mismatch");
  System.out.println("PASS " + checks + " gain, mode, exclusion and annotation checks (API stand-ins).");
 }
}'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit-jar", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    compiler = [shutil.which("javac")] if shutil.which("javac") else ["java", "--module", "jdk.compiler/com.sun.tools.javac.Main"]
    with tempfile.TemporaryDirectory(prefix="vab-tests-") as directory:
        temporary = Path(directory)
        for name, contents in STUBS.items():
            path = temporary / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(contents)
        (temporary / "MixTests.java").write_text(HARNESS)
        sources = [*root.joinpath("java").rglob("*.java"), *temporary.rglob("*.java")]
        classes = temporary / "classes"
        classes.mkdir()
        subprocess.run([*compiler, "--release", "17", "-g", "-d", str(classes),
                        *map(str, sources)], check=True)
        subprocess.run(["java", "-cp", str(classes), "MixTests"], check=True)
        if args.emit_jar:
            output = args.emit_jar.resolve()
            output.parent.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
                archive.writestr("META-INF/MANIFEST.MF", "Manifest-Version: 1.0\r\nImplementation-Version: 0.1.0\r\n\r\n")
                for path in sorted(classes.joinpath("com/memesnjunk/viewpointaudio").rglob("*.class")):
                    archive.write(path, path.relative_to(classes).as_posix())
            print("Experimental binary:", output)


if __name__ == "__main__":
    main()

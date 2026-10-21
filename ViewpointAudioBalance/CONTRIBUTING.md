# Contributing and building

Use a legitimate Build 42.21 installation, the separately installed Viewpoint/ZombieBuddy versions listed in mod.info and a disposable save. Keep Java 25 available for builds against the real game API (the supplied engine classes have major version 69).

Build with real dependencies:

```text
python build.py --game-jar /path/to/projectzomboid.jar --viewpoint-jar /path/to/Viewpoint.jar --zombiebuddy-jar /path/to/ZombieBuddy.jar --javac /path/to/jdk-25/bin/javac
```

Quote paths containing spaces. The build emits only this project's production classes into the client JAR. Dependency JARs are compile-only and must not be copied into the distribution.

Run portable logic tests with `python tests/run_tests.py`; they use generated minimal signature stand-ins and JDK 17 or newer. They verify mode/group routing, exclusions, bounds, mute and repeated-calculation behavior, not ZombieBuddy weaving or FMOD output. The optional `--emit-jar` supports the experimental environment; release candidates should be rebuilt against real dependencies and tested in-game.

Use descriptive names, four-space indentation and comments for non-obvious integration decisions. Keep original-volume input immutable; do not write clip.volume or native saved preferences. Submit patches with TESTING.md results and update documentation/changelog. No public repository has been created yet.

Bug reports should include game/Viewpoint/agent versions, active audio mods, exact sounds, gains, mode and relevant console lines. Do not claim compatibility or audible correctness solely from unit tests. Keep third-party binaries and extracted code/assets out of submissions.

#!/usr/bin/env python3
"""Build against installed APIs with JDK 25; no dependency binaries are bundled."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game-jar", type=Path, required=True)
    parser.add_argument("--viewpoint-jar", type=Path, required=True)
    parser.add_argument("--zombiebuddy-jar", type=Path, required=True)
    parser.add_argument("--javac", default="javac", help="Path to JDK 25 javac")
    args = parser.parse_args()
    dependencies = [args.game_jar, args.viewpoint_jar, args.zombiebuddy_jar]
    for path in dependencies:
        if not path.is_file():
            parser.error("Missing dependency: " + str(path))
    root = Path(__file__).resolve().parent
    sources = sorted((root / "java").rglob("*.java"))
    output = root / "42/media/java/client/ViewpointAudioBalance.jar"
    with tempfile.TemporaryDirectory(prefix="vab-build-") as directory:
        classes = Path(directory) / "classes"
        classes.mkdir()
        subprocess.run([args.javac, "--release", "17", "-g", "-d", str(classes),
                        "-classpath", os.pathsep.join(str(p.resolve()) for p in dependencies),
                        *[str(p) for p in sources]], check=True)
        output.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("META-INF/MANIFEST.MF",
                             "Manifest-Version: 1.0\r\nImplementation-Version: 0.1.0\r\n\r\n")
            for path in sorted((classes / "com/memesnjunk/viewpointaudio").rglob("*.class")):
                archive.write(path, path.relative_to(classes).as_posix())
    print(output)


if __name__ == "__main__":
    main()

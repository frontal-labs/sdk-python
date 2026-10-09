#!/usr/bin/env python3
"""Smoke-check the built wheel and source distribution."""

from __future__ import annotations

import os
import subprocess
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
VERSION = "1.0.0"


def main() -> None:
    wheels = list(DIST.glob("frontal-*.whl"))
    sdists = list(DIST.glob("frontal-*.tar.gz"))
    if len(wheels) != 1 or len(sdists) != 1:
        raise SystemExit(
            "expected one frontal wheel and one source distribution in dist/"
        )

    wheel = wheels[0]
    with zipfile.ZipFile(wheel) as archive:
        names = set(archive.namelist())
        metadata_path = next(
            (name for name in names if name.endswith(".dist-info/METADATA")), None
        )
        if metadata_path is None:
            raise SystemExit("wheel is missing distribution metadata")
        metadata = archive.read(metadata_path).decode("utf-8")
        if f"Version: {VERSION}\n" not in metadata:
            raise SystemExit(f"wheel metadata does not declare version {VERSION}")
        if "frontal_sdk/py.typed" not in names:
            raise SystemExit("wheel is missing frontal_sdk/py.typed")

    with tempfile.TemporaryDirectory(prefix="frontal-wheel-smoke-") as temp_dir:
        environment = os.environ.copy()
        environment["PYTHONPATH"] = os.pathsep.join(
            [str(wheel), environment.get("PYTHONPATH", "")]
        )
        subprocess.run(
            [
                sys.executable,
                "-c",
                "import frontal_sdk; assert frontal_sdk.__version__ == '1.0.0'",
            ],
            cwd=temp_dir,
            env=environment,
            check=True,
        )

    with tarfile.open(sdists[0], "r:gz") as archive:
        if not any(
            name.startswith(f"frontal-{VERSION}/frontal_sdk/")
            for name in archive.getnames()
        ):
            raise SystemExit("source distribution is missing the SDK package")

    print(f"validated built frontal {VERSION} wheel and source distribution")


if __name__ == "__main__":
    main()

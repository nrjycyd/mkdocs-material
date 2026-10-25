"""Read and validate the two version files used by builds and releases."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_versions():
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    revision = (ROOT / "IMAGE_REVISION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)", version):
        raise ValueError("VERSION must contain a stable version such as 9.8.0")
    if not re.fullmatch(r"[1-9][0-9]*", revision):
        raise ValueError("IMAGE_REVISION must contain a positive integer")
    return version, revision


if __name__ == "__main__":
    version, revision = read_versions()
    print(f"base={version}")
    print(f"release=v{version}-r{revision}")

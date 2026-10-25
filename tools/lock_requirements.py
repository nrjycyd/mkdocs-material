"""Lock the complete Python 3.11 dependency set for both container architectures."""

import argparse
import shutil
import subprocess
import tempfile
from pathlib import Path

from versions import ROOT, read_versions

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Fail if the committed lock is stale")
    mode.add_argument("--upgrade", action="store_true", help="Update compatible transitive dependencies")
    args = parser.parse_args()
    version, _ = read_versions()
    lock = ROOT / "requirements.txt"
    with tempfile.TemporaryDirectory(prefix="mkdocs-lock-") as directory:
        output = Path(directory) / "requirements.txt" if args.check else lock
        if args.check:
            shutil.copyfile(lock, output)
        command = [
            "uv", "pip", "compile", "requirements.in", "-",
            "--python-version", "3.11", "--universal", "--generate-hashes",
            "--default-index", "https://pypi.org/simple", "--no-header", "--quiet",
            "--output-file", str(output),
        ]
        if args.upgrade:
            command.append("--upgrade")
        subprocess.run(
            command,
            input=f"mkdocs-material[git,imaging,recommended]=={version}\n",
            text=True,
            cwd=ROOT,
            check=True,
        )
        if args.check and output.read_bytes() != lock.read_bytes():
            raise SystemExit("Dependency lock is stale; run python tools/lock_requirements.py")
    print("Dependency lock is current" if args.check else "Updated requirements.txt")

"""Build an offline fixture and inspect rendered output, not just exit codes."""

import json
import shutil
import subprocess
import sys
import tempfile
from importlib.metadata import entry_points
from pathlib import Path

EXPECTED_PLUGINS = {
    "search", "macros", "glightbox", "statistics", "table-reader",
    "markdown-exec", "markmap", "plantuml", "literate-nav", "mkdocstrings",
    "minify", "git-revision-date-localized", "git-committers",
}


def check():
    plugins = {entry.name: entry for entry in entry_points(group="mkdocs.plugins")}
    missing = EXPECTED_PLUGINS - plugins.keys()
    if missing:
        raise RuntimeError(f"Missing plugins: {sorted(missing)}")
    # Git plugins are imported here; their repository/API operations require a real site.
    for name in sorted(EXPECTED_PLUGINS):
        plugins[name].load()

    with tempfile.TemporaryDirectory(prefix="mkdocs-smoke-") as directory:
        root = Path(directory)
        shutil.copyfile(Path(__file__).with_name("mkdocs.yml"), root / "mkdocs.yml")
        docs = root / "docs"
        docs.mkdir()
        (root / "sample_api.py").write_text(
            'def greet(name: str) -> str:\n'
            '    """SMOKE_API_OK."""\n'
            '    return f"Hello {name}"\n', encoding="utf-8",
        )
        (docs / "data.csv").write_text("name,value\nSMOKE_TABLE_OK,42\n", encoding="utf-8")
        (docs / "index.md").write_text(
            '# Smoke test\n\n{{ smoke_message }}\n\n'
            '```python exec="on"\nprint("SMOKE_" + "EXEC_" + str(6 * 7))\n```\n\n'
            '{{ read_csv("docs/data.csv") }}\n\n'
            '::: sample_api.greet\n', encoding="utf-8",
        )
        subprocess.run(
            [sys.executable, "-X", "utf8", "-m", "mkdocs", "build", "--strict"],
            cwd=root, check=True,
        )
        html = (root / "site" / "index.html").read_text(encoding="utf-8")
        for marker in ("SMOKE_MACRO_OK", "SMOKE_EXEC_42", "SMOKE_TABLE_OK", "SMOKE_API_OK"):
            if marker not in html:
                raise RuntimeError(f"Rendered page is missing {marker}")
        if "<table" not in html:
            raise RuntimeError("CSV was not rendered as an HTML table")
        index = json.loads((root / "site" / "search" / "search_index.json").read_text(encoding="utf-8"))
        if not any("SMOKE_EXEC_42" in entry.get("text", "") for entry in index["docs"]):
            raise RuntimeError("Search index does not contain the executed code output")
    print("Smoke test passed: plugin imports, strict build, macros, code execution, CSV, API and search")


if __name__ == "__main__":
    check()

#!/usr/bin/env python3
"""Generate simple documentation indexes from Markdown files."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
paths = sorted(
    p
    for p in ROOT.rglob("*.md")
    if ".git" not in p.parts
    and ".venv" not in p.parts
    and ".pytest_cache" not in p.parts
    and ".mypy_cache" not in p.parts
    and ".ruff_cache" not in p.parts
    and "node_modules" not in p.parts
    and "target" not in p.parts
    and "build" not in p.parts
    and "dist" not in p.parts
    and p.name != "PLAN.md"
)
documents = [
    {"path": p.relative_to(ROOT).as_posix(), "title": p.stem.replace("_", " ")}
    for p in paths
]
manifest = {
    "name": "Frontal Python SDK",
    "language": "Python",
    "version": "2.0.0",
    "status": "stable",
    "documents": documents,
}
content = json.dumps(manifest, indent=2) + "\n"
(ROOT / "docs/mcp.json").write_text(content, encoding="utf-8")
(ROOT / "mcp.json").write_text(content, encoding="utf-8")

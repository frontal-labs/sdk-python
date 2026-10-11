#!/usr/bin/env python3
"""Generate simple documentation indexes from tracked Markdown files."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def tracked_markdown() -> list[Path]:
    """List tracked Markdown files so local scratch files never leak in."""
    output = subprocess.run(
        ["git", "ls-files", "--", "*.md"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return [ROOT / line for line in output.splitlines() if line]


paths = sorted(p for p in tracked_markdown() if p.name != "PLAN.md")
documents = [
    {"path": p.relative_to(ROOT).as_posix(), "title": p.stem.replace("_", " ")}
    for p in paths
]
manifest = {
    "name": "Frontal Python SDK",
    "language": "Python",
    "version": "1.0.0",
    "status": "stable",
    "documents": documents,
}
content = json.dumps(manifest, indent=2) + "\n"
(ROOT / "docs/mcp.json").write_text(content, encoding="utf-8")
(ROOT / "mcp.json").write_text(content, encoding="utf-8")

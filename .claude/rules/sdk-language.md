---
paths:
  - "**/*.py"
---

# Python changes

Support Python 3.9–3.12. Keep the import package frontal_sdk separate from the PyPI distribution name frontal. Use HTTPX, Pydantic v2, uv/Hatchling, Ruff, mypy, pytest, anyio, and offline RESPX tests. Treat contracts as endpoint authority.

Follow the repository's `AGENTS.md` and `CLAUDE.md`. Use the relevant installed language skill under `.claude/skills/`. Add deterministic, offline tests for behavior changes, and run the repository's relevant format, lint, type/build, and contract checks.

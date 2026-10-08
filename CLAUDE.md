@AGENTS.md

# Python SDK repository instructions

Read `AGENTS.md` first for repository layout, project conventions, and contract rules. Read `README.md` and the relevant design docs before changing public SDK behavior.

## Contract and compatibility

Support Python 3.9–3.12. Keep the import package frontal_sdk separate from the PyPI distribution name frontal. Use HTTPX, Pydantic v2, uv/Hatchling, Ruff, mypy, pytest, anyio, and offline RESPX tests. Treat contracts as endpoint authority.

Do not add public endpoints, wire fields, or behavior unsupported by the committed contracts. Keep credentials, tokens, and customer data out of source, logs, fixtures, and examples. Make the smallest compatible change and update documentation/examples when public behavior changes.

## Skills

Use the matching skill in `.claude/skills/` when its topic applies. Skills are also linked from `.agents/skills/`; source files live in `skills/` and selected upstream sources are recorded in `skills/SOURCES.md`.

## Verification commands

Run only the commands relevant to the change; do not claim verification unless it was run.

```sh
uv run ruff format --check .
uv build
uv run ruff check .
uv run mypy --strict
uv run python -m pytest
uv run python scripts/check_contracts.py
```

Review the current diff and identify affected modules, public behavior, and relevant contract entries. Run only checks relevant to the changes, choosing from the repository commands below. Do not edit code unless I explicitly ask you to fix a failure. Report checks run and their results.

```sh
uv run ruff format --check .
uv build
uv run ruff check .
uv run mypy --strict
uv run python -m pytest
uv run python scripts/check_contracts.py
```

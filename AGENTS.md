# Frontal Python SDK - Agent Instructions

## Repository scope

This repository contains the Python SDK. The committed endpoint inventory and
OpenAPI snapshots are authoritative for endpoint methods and paths. Do not
change the public HTTP API, edit the OpenAPI snapshots, or invent endpoint
methods. Keep the client and endpoint methods hand-written; use the contract
checker to catch drift.

## Layout

- `frontal_sdk/` — installable package with `core`, `models`, and `resources`.
- `tests/` — pytest suite using RESPX at the HTTPX layer; no live API is needed.
- `contracts/openapi/` — shared OpenAPI snapshots.
- `contracts/sdk-endpoints.json` — endpoint inventory and contract source.
- `docs/`, `examples/`, and `templates/` — Python developer material.

## Python conventions

The PyPI distribution is `frontal`; its import package is `frontal_sdk/`.
Support Python 3.9–3.12. Shared transport behavior lives in
`frontal_sdk/core`, Pydantic v2 boundary models live in `frontal_sdk/models`,
and service methods live in `frontal_sdk/resources`. The sync and async
unified clients are in `frontal_sdk/client.py`. Ship inline types and
`frontal_sdk/py.typed`.

- Use `uv` with the Hatchling build backend, HTTPX, Pydantic v2, Ruff, mypy,
  pytest, and anyio as configured in `pyproject.toml` and `uv.lock`.
- Keep resource methods in their domain modules and shared transport behavior
  in `core`.
- Keep Markdown under `docs/`, except for repository-level README and
  community files.
- Add offline tests and runnable examples with implemented behavior.
- Never check in credentials or customer data.

## Quality commands

```bash
uv sync --extra dev
uv run ruff format --check .
uv build
uv run ruff check .
uv run mypy --strict
uv run python -m pytest
uv run python scripts/check_contracts.py
```

CI runs format, build, lint, type check, tests, examples, docs, and the
contract gate across supported Python versions. The README Python fences are
executed with mocked HTTP responses.

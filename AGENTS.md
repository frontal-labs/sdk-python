# Frontal Python SDK - Agent Instructions

## Repository scope

This repository is the Python SDK. The package-level client, shared runtime, service clients, and endpoint catalogs are present. Treat the committed contract snapshots as the source for endpoint shapes, and do not invent public methods.

## Layout

- `frontal_sdk/` — installable package with shared `utils` and the 17 service domains.
- `tests/` — repository test suite; keep test helpers here unless they are deliberately designed as supported SDK APIs.
- `contracts/openapi/` — shared OpenAPI snapshots.
- `contracts/sdk-endpoints.json` — service endpoint inventory for future conformance reporting.
- `docs/`, `examples/`, and `templates/` — Python-specific developer material and starter projects.

## Python conventions

Python ships as one `frontal-sdk` distribution with the installable package at `frontal_sdk/`. Shared runtime code lives under `frontal_sdk/utils`, the unified client in `frontal_sdk/client.py`, API boundary types in `frontal_sdk/api_types.py`, shared service client behavior in `frontal_sdk/services/base.py`, and endpoint models and operations under `frontal_sdk/services/<service>`. Keep public typing in the package, target Python 3.10+, and use Ruff for formatting and linting.

- Use the Python toolchain documented in the root README and document direct native commands.
- Keep service models and operations in the matching service module. Put shared transport behavior in `core`.
- Keep Markdown documentation under `docs/`, not inside the import package.
- Add tests, docs, and runnable examples when the matching API is implemented.
- Never check in credentials or customer data.

## Key commands

```bash
ruff format --check .
ruff check .
mypy
python -m pytest
python -m build
```

Run the local HTTP integration suite with `python -m pytest`. The contract and docs index helpers are Python 3 standard-library maintenance scripts; they do not add Python as a runtime dependency for the SDK.

# Python developer guide

## Tooling

Use Python 3.10 or later and the native commands listed in [`README.md`](../README.md). The SDK runtime is written in Python. Contract and documentation maintenance scripts use Python's standard library.

## Change placement

Keep transport concerns in `frontal_sdk/core/`, shared request and response types in `frontal_sdk/models/`, resource methods in their matching `frontal_sdk/resources/<domain>.py` module, and client construction in `frontal_sdk/client.py`. The package root exports stable shared types. Put tests in root `tests/` and documentation under `docs/`. Regenerate resources from `contracts/sdk-endpoints.json` with `python3 scripts/generate_resources.py` after contract changes.

## Contract workflow

`contracts/openapi/` and `contracts/sdk-endpoints.json` are shared contract inputs. Run `python3 scripts/check_contracts.py` to validate snapshots, `python3 scripts/generate_resources.py` to regenerate endpoint methods, and `python3 scripts/generate_docs_manifest.py` after changing Markdown documentation.

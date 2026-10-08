# Python developer guide

## Tooling

Use Python 3.10 or later and the native commands listed in [`README.md`](../README.md). The SDK runtime is written in Python. Two small repository maintenance scripts use Python 3's standard library to parse contract JSON and build the documentation index.

## Change placement

Keep shared transport concerns in `frontal_sdk/utils/`, reusable service client behavior in `frontal_sdk/services/base.py`, the unified client in `frontal_sdk/client.py`, and endpoint behavior in its matching `frontal_sdk/services/<service>/` module. Put API boundary types in `frontal_sdk/api_types.py`. The package root exports the stable public API. Put tests in root `tests/`, and keep package documentation under `docs/`. Update API types, examples, and the generated migration matrix with each implemented operation.

## Contract workflow

`contracts/openapi/` and `contracts/sdk-endpoints.json` are shared input snapshots. Run `python scripts/check_contracts.py` to check the snapshot files and `python scripts/generate_docs_manifest.py` after changing Markdown documentation.

# Python SDK package structure

## Goal

Keep one `frontal-sdk` distribution with the installable `frontal_sdk/` package at the repository root. Organize shared infrastructure in `utils/` and service APIs in `services/`.

## Package layout

- `frontal_sdk/client.py` — unified `Frontal` client.
- `frontal_sdk/api_types.py` — public JSON API boundary types.
- `frontal_sdk/utils/` — configuration, errors, HTTP transport, and endpoint descriptors.
- `frontal_sdk/services/base.py` — reusable base behavior for service clients.
- `frontal_sdk/services/<service>/` — service clients and endpoint catalogs.
- `tests/`, `docs/`, `examples/`, `templates/`, and `contracts/` — repository material outside the runtime package.

## Conventions

Use Python 3.10+, keep the `py.typed` marker inside the installable package, and use Ruff for formatting and linting. Keep endpoint shapes grounded in the committed API contracts. Add service request/response models and convenience methods only alongside their matching API implementation.

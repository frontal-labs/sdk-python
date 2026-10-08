# Frontal Python SDK

![Frontal Banner](./banner.png)

**Frontal client library for Python.**

The Python SDK provides a shared authenticated HTTP transport, a unified `Frontal` client, and endpoint catalogs for all REST service packages. The transport handles timeouts, safe GET retries, structured API errors, JSON, multipart uploads, raw responses, and server-sent events.

> **Current status:** the package-level client, shared HTTP runtime, service clients, endpoint catalogs, and local-server tests are present. Service clients currently dispatch through typed endpoint catalogs; dedicated service request/response models are still to come. The contract snapshots are the source of endpoint shapes.

## Repository map

| Path | Purpose |
| --- | --- |
| `frontal_sdk/` | Installable Python package with a unified client, shared utilities, and service subpackages |
| `tests/` | Pytest coverage for the shared client and HTTP transport |
| `contracts/` | OpenAPI snapshots, endpoint inventory, and this repository's conformance reports |
| `docs/` | Python architecture, service, onboarding, testing, and release guidance |
| `examples/` | Python integration guide and runnable examples |
| `templates/` | Python application starter layouts |
| `scripts/` | Contract and documentation maintenance utilities |
| `.github/` | Python CI, security analysis, and contribution templates |

## Install

For local development, install the package and its tools from the repository root:

```bash
python -m pip install -e ".[dev]"
```

The package is not published yet. After release, install it with `python -m pip install frontal-sdk`.

## Quickstart

Set `FRONTAL_API_KEY` in the process environment, then use the package-level client and a service endpoint:

```python
from frontal_sdk import Frontal
from frontal_sdk.services.ai import AiEndpoint

client = Frontal.from_env()
health = client.ai.call(AiEndpoint.GET_HEALTH)
```

## Development

Requirements: Python 3.10 or later. Check the interpreter with `python --version` and `python -m pip --version`.

```bash
ruff format --check .
ruff check .
mypy
python -m pytest
python -m build
```

The pytest suite exercises the HTTP transport and client using a local server. It does not require live API credentials.

See [`CONTRIBUTING.md`](./CONTRIBUTING.md), [`docs/ONBOARDING.md`](./docs/ONBOARDING.md), [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md), and [`AGENTS.md`](./AGENTS.md).

## License

Apache-2.0. See [`LICENSE.md`](./LICENSE.md).

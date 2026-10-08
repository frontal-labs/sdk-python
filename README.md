# Frontal Python SDK

![Frontal Banner](./banner.png)

**Frontal client library for Python.**

The Python SDK provides a unified `Frontal` client with typed resource methods for every operation in the committed endpoint inventory. The shared transport handles timeouts, safe GET retries, structured API errors, JSON, multipart uploads, raw responses, and server-sent events. Public APIs are typed and the distribution includes a `py.typed` marker for downstream type checkers.

> **Current status:** resource methods cover all 370 operations in `contracts/sdk-endpoints.json`. Request and response payloads use the typed JSON boundary because the committed inventory does not include operation-specific schemas for these endpoints.

The client accepts an explicit API key or can read `FRONTAL_API_KEY` and `FRONTAL_API_URL` from the environment. Configuration is validated when the client is created; custom headers can be supplied as any read-only or mutable mapping and are copied into the client configuration.

## Repository map

| Path | Purpose |
| --- | --- |
| `frontal_sdk/core/` | Client configuration, HTTP transport, errors, and operation descriptors |
| `frontal_sdk/models/` | JSON boundary types, query parameters, uploads, and server events |
| `frontal_sdk/resources/` | Typed resource methods grouped by API domain |
| `tests/` | Pytest coverage for the shared client and HTTP transport |
| `contracts/` | OpenAPI snapshots, endpoint inventory, and this repository's conformance reports |
| `docs/` | Python architecture, resource, onboarding, testing, and release guidance |
| `examples/` | Python integration guide and runnable examples |
| `templates/` | Python-first starter projects for CLI, batch, and asyncio setups |
| `scripts/` | Contract and documentation maintenance utilities |
| `.github/` | Python CI, security analysis, and contribution templates |

## Install

For local development, install the package and its tools from the repository root:

```bash
python -m pip install -e ".[dev]"
```

The package is not published yet. After release, install it with `python -m pip install frontal-sdk`.

## Quickstart

Set `FRONTAL_API_KEY` in the process environment, then use the package-level client and a resource method:

```python
from frontal_sdk import Frontal
client = Frontal.from_env()
health = client.ai.get_health()
```

Resource methods accept `query=` for URL parameters, `body=` for JSON request bodies, and explicit arguments for path placeholders. For example, `client.agents.get_agents_by_param_1("agent_123")` reads one agent.

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

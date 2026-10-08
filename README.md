# Frontal Python SDK

![Frontal Banner](./banner.png)

The `frontal` package provides synchronous and asynchronous Python clients for
the Frontal API. Services are available on the client as typed attributes such
as `client.ai`, `client.agents`, and `client.workflows`.

## Install

Python 3.9–3.12 is supported.

```bash
pip install frontal
# or
uv add frontal
```

## Quickstart

Set `FRONTAL_API_KEY`, then make the first request:

```python
from frontal_sdk import Frontal
with Frontal() as client:
    health = client.ai.get_health()
    print(health)
```

The async client exposes the same services and operation methods:

```python
import asyncio
from frontal_sdk import AsyncFrontal
async def main():
    async with AsyncFrontal() as client:
        return await client.ai.get_health()
print(asyncio.run(main()))
```

`FRONTAL_API_URL`, `FRONTAL_ENV`, and `FRONTAL_DEBUG` configure the URL,
environment header, and debug logging. The SDK does not load `.env` files.

## What is included

- All 370 operations in `contracts/sdk-endpoints.json`, grouped by service.
- HTTPX sync and async transports with bounded GET retries, request IDs,
  pagination helpers, polling, raw bytes, multipart uploads, and SSE streams.
- Pydantic v2 request models and validation for JSON-compatible payloads.
- A structured error hierarchy with status, code, request ID, and retryability.
- Inline package typing, including `py.typed`.

The OpenAPI snapshots define the operation inventory but do not include
service-specific request and response schemas for most endpoints. The SDK
does not guess those payload shapes; define request models with `APIModel` and
use `PageResult[T]` for paginated responses where applicable.

## Development

Install the locked development environment with `uv`:

```bash
uv sync --extra dev
```

Run the CI checks locally:

```bash
uv run ruff format --check .
uv build
uv run ruff check .
uv run mypy --strict
uv run python -m pytest
uv run python scripts/check_contracts.py
```

The tests use RESPX at the HTTPX layer and do not need a running API or live
credentials. See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md),
[`docs/TESTING.md`](docs/TESTING.md), and [`docs/PUBLISHING.md`](docs/PUBLISHING.md).

## License

Apache-2.0. See [`LICENSE.md`](LICENSE.md).

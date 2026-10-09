# Frontal Python SDK

![Frontal Banner](./banner.png)

[![skills.sh](https://skills.sh/b/frontal-labs/sdk-python)](https://skills.sh/frontal-labs/sdk-python)

The `frontal` package provides synchronous and asynchronous Python clients for
the Frontal API. Services are available on the client as typed attributes such
as `client.ai`, `client.agents`, `client.functions`, and `client.workflows`.

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
    result = client.ai.generate_text(
        {"model": "frontal-ai-fast", "prompt": "Say hello."}
    )
    print(result.text)
```

The async client exposes the same services and operation methods:

```python
import asyncio
from frontal_sdk import AsyncFrontal


async def main():
    async with AsyncFrontal() as client:
        return await client.ai.generate_text(
            {"model": "frontal-ai-fast", "prompt": "Say hello."}
        )


print(asyncio.run(main()))
```

`FRONTAL_API_URL`, `FRONTAL_ENV`, and `FRONTAL_DEBUG` configure the URL,
environment header, and debug logging. The SDK does not load `.env` files.

## What is included

- All 383 operations in `contracts/sdk-endpoints.json`, grouped by service.
- HTTPX sync and async transports with bounded GET retries, request IDs,
  pagination helpers, polling, raw bytes, multipart uploads, and SSE streams.
- Pydantic v2 request models and validation for JSON-compatible payloads.
- A structured error hierarchy with status, code, request ID, transient status,
  and an explicit `safe_to_retry` signal.
- Inline package typing, including `py.typed`.

Streaming POST requests default to no retries because a connection failure can
occur after the server has accepted the request. Pass an explicit retry count
only when replaying that operation is safe. If you provide an `httpx.Client` or
`httpx.AsyncClient`, you retain ownership of its lifecycle and timeout settings.
For JSON writes, omitting `body` sends no request body; pass `body=None` to send
the JSON value `null`, and `body={}` to send an empty JSON object.

The endpoint inventory records the SDK's hand-written routes. OpenAPI snapshots
provide an additional contract baseline, but they omit the Functions routes
and most endpoint-specific request and response schemas. The Functions models
follow the TypeScript Functions package; other unmodeled operation payloads
use the recursive `JSONValue` type.

The [Functions API guide](docs/FUNCTIONS.md) covers function definitions,
versions, deployment, invocation, execution results, and cancellation.

The SDK uses resource-oriented names and semantic path arguments.

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

## Agent skills

Install this repository's Python-specific agent skills with the [skills CLI](https://skills.sh/docs/cli):

```bash
npx skills add frontal-labs/sdk-python
```

## License

Apache-2.0. See [`LICENSE.md`](LICENSE.md).

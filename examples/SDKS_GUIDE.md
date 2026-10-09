# Python SDK integration guide

The PyPI distribution is `frontal`; import its `frontal_sdk` package. For
development inside this repository, install the locked environment with:

```bash
uv sync --extra dev
```

## Create and close clients

Pass `api_key` directly, or set `FRONTAL_API_KEY` in the process environment.
The client also reads `FRONTAL_API_URL`, `FRONTAL_ENV`, and `FRONTAL_DEBUG`.
Python does not load `.env` files automatically.

```python
from frontal_sdk import Frontal

with Frontal() as client:
    result = client.ai.generate_text(
        {"model": "frontal-ai-fast", "prompt": "Say hello."}
    )
    print(result.text)
```

For asyncio applications, use `AsyncFrontal`; do not call the synchronous
client from an async event loop:

```python
import asyncio
from frontal_sdk import AsyncFrontal


async def main() -> None:
    async with AsyncFrontal() as client:
        result = await client.ai.generate_text(
            {"model": "frontal-ai-fast", "prompt": "Say hello."}
        )
        print(result.text)


asyncio.run(main())
```

## Service methods

Clients expose `ai`, `agents`, `workflows`, `audit`, `auth`, `billing`, `blob`,
`connectors`, `data`, `governance`, `lineage`, `observability`, `ontology`,
`pipelines`, `schedules`, and `webhooks`. The first three also
provide high-level helpers and validated builders. For example, create an agent
with `client.agents.define(name).trigger(event).can_read(entity).create()` or
define a workflow with `client.workflows.define(name).manual().task(...).create()`.
Then use the returned identifier with `client.agents.use(id)` or
`client.workflows.use(id)` to message, inspect, trigger, or poll runs.

SDK operations use resource-oriented method names and semantic path
arguments where the contract provides them. Pass query parameters as `query=`,
JSON request values as `body=`, multipart uploads as `parts=`, and raw request
bodies as `data=` plus `content_type=`. Most operations return JSON values
because the OpenAPI snapshot does not define a specific response schema for
each operation. See [API resources](../docs/RESOURCES.md) and
[examples](./README.md).

Sync streams use `for`; async streams use `async for`. AI `stream_text()` yields
typed text and lifecycle parts. Agent `watch(run_id)` yields raw
`ServerEvent` values. Long-running agent runs and workflow executions can be
observed with their accessors' `wait_for_completion()` methods.

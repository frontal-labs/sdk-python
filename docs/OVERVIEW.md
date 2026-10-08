# Python SDK overview

The `frontal` distribution installs the `frontal_sdk` package. It supports
Python 3.9–3.12 and provides synchronous and asynchronous clients, typed AI
helpers, Pydantic v2 models, and hand-written methods for every operation in the
committed endpoint inventory.

## Install and connect

Install from PyPI with `uv add frontal` or `python -m pip install frontal`.
Pass a key directly or set `FRONTAL_API_KEY` before creating a client:

```python
from frontal_sdk import Frontal

with Frontal() as client:
    result = client.ai.generate_text(
        {"model": "frontal-ai-fast", "prompt": "Say hello."}
    )
    print(result.text)
```

`AsyncFrontal` uses the same services with awaitable JSON and byte requests and
asynchronous iterators for streams:

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

Both clients read `FRONTAL_API_KEY`, `FRONTAL_API_URL`, `FRONTAL_ENV`, and
`FRONTAL_DEBUG` when the matching constructor argument is omitted. The default
API URL is `https://api.frontal.dev/v1`. Set `timeout` and `max_retries` on the
client to tune transport behavior. See [architecture](ARCHITECTURE.md) and
[resources](RESOURCES.md) for details.

## Services

Each client exposes the same service attributes:

`ai`, `agents`, `workflows`, `audit`, `auth`, `billing`, `blob`, `connectors`,
`data`, `governance`, `lineage`, `observability`, `ontology`, `pipelines`,
`sandbox`, `schedules`, and `webhooks`.

The AI service adds normalized helpers such as `generate_text`, `stream_text`,
`embed`, `generate_object`, `generate_speech`, `generate_image`,
`generate_video`, `transcribe`, `moderate`, and `rerank`. The agents and
workflows services include validated definition builders, accessors, polling,
and run or execution streams. Every service also exposes the hand-written
endpoint methods from the SDK inventory.

## Types and API boundaries

Public models are exported from `frontal_sdk` and `frontal_sdk.models`. The
client validates typed AI, agent, workflow, pagination, and error boundaries
with Pydantic. Many raw API operations have no operation-specific schema in the
OpenAPI snapshots, so their request and response values use the recursive
`JSONValue` type rather than guessed models. See [API resources](RESOURCES.md)
for route naming and payload conventions.

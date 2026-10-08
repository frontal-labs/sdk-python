# Asyncio client template

This starter uses `AsyncFrontal` and the SDK's native async HTTPX transport.
It bounds concurrent agent lookups with an asyncio semaphore and closes the
shared connection pool after all requests finish.

## Install

From this directory:

```bash
uv sync
```

`uv sync` installs `frontal>=1.0.0` from PyPI. To use the SDK source in this
repository checkout, follow the editable dependency instructions in
[`templates/README.md`](../README.md).

Set `FRONTAL_API_KEY`, then run:

```bash
uv run frontal-async agent_123 agent_456 --concurrency 4
```

The program prints one JSON object per agent ID. Set `FRONTAL_API_URL` to override the API URL.

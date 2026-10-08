# Asyncio client template

This starter uses `AsyncFrontal` and the SDK's native async HTTPX transport. It bounds concurrent requests with an asyncio semaphore.

## Install

From this directory:

```bash
uv sync
```

Set `FRONTAL_API_KEY`, then run:

```bash
uv run frontal-async agent_123 agent_456 --concurrency 4
```

The program prints one JSON object per agent ID. Set `FRONTAL_API_URL` to override the API URL.

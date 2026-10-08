# Asyncio client template

The Frontal SDK is synchronous. This starter shows how to call it from an asyncio program without blocking the event loop: each request runs in `asyncio.to_thread`, and a semaphore bounds concurrent requests.

## Install

From this directory in the SDK repository:

```bash
python -m pip install -e ../..
python -m pip install -e .
```

Set `FRONTAL_API_KEY`, then run:

```bash
frontal-async agent_123 agent_456 --concurrency 4
```

The program prints one JSON object per agent ID. Set `FRONTAL_API_URL` to override the API URL. For a fully asynchronous HTTP client, use an SDK with native async transport when one is available; this template adapts the current synchronous SDK.

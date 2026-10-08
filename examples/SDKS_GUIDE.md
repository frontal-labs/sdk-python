# Frontal Python SDK guide

This guide shows the package-level client and generic endpoint dispatch. Use the endpoint catalogs instead of guessing paths or method names.

## Toolchain

Python 3.10 or later. See the root README for direct build and quality commands.

## Configuration

Set `FRONTAL_API_KEY` to a key beginning with `frt_`. `FRONTAL_API_URL` defaults to `https://api.frontal.dev/v1`. Python does not load `.env` files automatically. Read values from `os.environ` or configure environment injection in your process manager.

## Basic request

Set `FRONTAL_API_KEY`, then create a client and call an endpoint from its service catalog:

```python
from frontal_sdk import Frontal
from frontal_sdk.services.ai import AiEndpoint

client = Frontal.from_env()
health = client.ai.call(AiEndpoint.GET_HEALTH)
```

## Module map

- `core` — shared transport, configuration, errors, retries, and response handling.
- `sdk` — unified `Frontal` client and service accessors.
- `services` — agents, ai, audit, auth, billing, blob, connectors, data, governance, lineage, observability, ontology, pipelines, sandbox, schedules, webhooks, workflows.

See [`docs/ARCHITECTURE.md`](../docs/ARCHITECTURE.md) and [`docs/SERVICES.md`](../docs/SERVICES.md) for package status and service guidance. Add endpoint examples alongside tests when operations gain dedicated methods and models.

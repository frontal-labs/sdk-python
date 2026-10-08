---
name: frontal-sdk-python
description: Build Python integrations with Frontal or change, test, and document the Frontal Python SDK.
---

# Frontal Python SDK

Use this skill both for application code using Frontal and for changes inside this SDK. Confirm current call signatures and supported fields in `frontal_sdk/` and the repository docs. `contracts/sdk-endpoints.json` plus `contracts/openapi/` are authoritative for routes and wire behavior.

## Choose a client

The `frontal` distribution exposes the `frontal_sdk` import package. Use `Frontal` for synchronous programs and `AsyncFrontal` for async programs. Both expose service attributes such as `client.ai`, `client.agents`, and `client.workflows`.

```python
from frontal_sdk import Frontal

with Frontal() as client:
    result = client.ai.generate_text(
        {"model": "frontal-ai-fast", "prompt": "Say hello."}
    )
```

For async work, use `async with AsyncFrontal() as client` and await operations. Avoid mixing sync calls into an async request path. Pass configuration directly when it is already available; environment defaults are `FRONTAL_API_KEY`, `FRONTAL_API_URL`, `FRONTAL_ENV`, and `FRONTAL_DEBUG`. The SDK does not load `.env` files itself.

## Models, errors, and long-running work

- Shared HTTPX behavior belongs in `frontal_sdk/core`; Pydantic v2 boundary models belong in `frontal_sdk/models`; domain methods belong in `frontal_sdk/resources`.
- Preserve typed return models and validation. Do not add speculative fields or route methods; use the contract inventory and contract checker.
- Handle the SDK's typed API/network errors at the appropriate boundary. Keep request IDs when logging diagnostics, and never log credentials or customer payloads by default.
- Use the provided pagination, polling, and SSE helpers when they match the endpoint. Close sync and async clients with their respective context managers.
- Do not retry writes without a contract-supported idempotency strategy.

## Change the SDK

Keep client and resource methods hand-written. Do not generate public methods from OpenAPI. Add shared transport behavior to `frontal_sdk/core`, typed boundary models to `frontal_sdk/models`, and service methods to the matching `frontal_sdk/resources` module. Preserve Python 3.9–3.12 compatibility, inline typing, and `frontal_sdk/py.typed`. Follow the configured HTTPX, Pydantic v2, Ruff, mypy, pytest, and anyio versions in `pyproject.toml` and `uv.lock`.

For endpoint changes, consult contracts, implement the method, and use `scripts/check_contracts.py` to catch coverage or drift. Add offline tests with RESPX at the HTTPX layer, including sync/async behavior as appropriate. Add examples only for working, implemented behavior; README Python fences are executed in CI.

## Tests and quality

Keep tests independent of live Frontal services and secrets. Use pytest and RESPX; use anyio patterns for async coverage. Cover request serialization, response validation, errors, pagination, resource cleanup, and contract alignment for the behavior changed.

Useful checks from the root:

```bash
uv sync --extra dev
uv run ruff format --check .
uv build
uv run ruff check .
uv run mypy --strict
uv run python -m pytest
uv run python scripts/check_contracts.py
```

Also review `AGENTS.md`, `docs/ARCHITECTURE.md`, `docs/RESOURCES.md`, and the focused guide under `docs/` before making structural changes.

# Python testing strategy

Tests live under `tests/` and are excluded from the SDK distribution. RESPX
intercepts HTTPX requests at the transport layer, so the suite needs no running
API or live credentials. It covers sync and async requests, retries, errors,
Pydantic body serialization, pagination, polling, uploads, raw responses, and
sync/async SSE streams.

The README Python fences are executed by pytest with a mocked health endpoint.
Examples have a separate offline smoke test. Run the full suite with:

```bash
uv sync --extra dev
uv run python -m pytest
```

Keep test helpers in `tests/` unless they are intentionally supported SDK APIs.

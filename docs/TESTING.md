# Python testing strategy

Tests live under `tests/` and are excluded from the SDK distribution. RESPX
intercepts HTTPX requests at the transport layer, so the suite needs no running
API or live credentials. It covers sync and async requests, retries, errors,
Pydantic body serialization, pagination, polling, uploads, raw responses, and
sync/async server-sent event streams.

The README Python fences run with a mocked `POST /ai/chat/completions`
response. Standalone examples have a separate offline smoke test, also backed
by RESPX. Run the suite with:

```bash
uv sync --extra dev
uv run python -m pytest
```

The test suite checks SDK behavior and executable documentation without
contacting Frontal services. Add a RESPX route for each new example that makes
an HTTP request.

Keep test helpers in `tests/` unless they are intentionally supported SDK APIs.

---
name: python-sync-async-clients
description: Implement and use the Frontal Python SDK's synchronous and asynchronous clients consistently.
---

# Python Sync and Async Clients

Use this skill when changing client lifecycle, sync/async parity, or request behavior in `sdk-python`.

- Use `Frontal` for sync applications and `AsyncFrontal` for async applications. Mirror public behavior where both client modes are supported.
- Use `with` and `async with` so HTTPX resources close deterministically. Do not block an async call path with sync network operations.
- Keep transport policy in `frontal_sdk/core` and domain operations in `frontal_sdk/resources`; avoid duplicating request handling in each service.
- Respect Python 3.9–3.12 support and the dependency versions pinned by `pyproject.toml`/`uv.lock`.
- Test sync behavior and async behavior independently where supported, including cancellation, timeouts, and cleanup. Use HTTP mocks; never require live credentials.
- Preserve the documented environment behavior; the SDK does not load `.env` files automatically.

Read `AGENTS.md`, `docs/ARCHITECTURE.md`, and `docs/RESOURCES.md` before changing package boundaries.

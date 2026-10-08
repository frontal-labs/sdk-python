---
name: frontal-sdk-python
description: Guidance for adding or reviewing integrations using the Frontal Python SDK.
---

# Frontal Python SDK

The package provides both `Frontal` and `AsyncFrontal`, a shared HTTPX transport, Pydantic v2 boundary models, and service methods for every operation in `contracts/sdk-endpoints.json`. Keep client and resource methods hand-written. Use the contract checker to validate endpoint coverage and drift; do not generate public methods.

## Configuration

Use `Frontal()` or `AsyncFrontal()` to read `FRONTAL_API_KEY`, `FRONTAL_API_URL`, `FRONTAL_ENV`, and `FRONTAL_DEBUG` from the process environment, or pass configuration directly. The SDK does not load `.env` files. See the root `.env.example` for local development conventions.

## Modules

See [the architecture guide](../../docs/ARCHITECTURE.md) and [resource guide](../../docs/RESOURCES.md).

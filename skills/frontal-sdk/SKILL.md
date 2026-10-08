---
name: frontal-sdk-python
description: Guidance for adding or reviewing integrations using the Frontal Python SDK.
---

# Frontal Python SDK

The package-level client, shared runtime primitives, service clients, and endpoint catalogs are implemented. Check the Python source before using an operation; an endpoint in `contracts/` does not guarantee a dedicated convenience method exists. Follow the idioms and toolchain documented in this repository.

## Configuration

Use `Frontal.from_env()` to read `FRONTAL_API_KEY` and optional `FRONTAL_API_URL` from the process environment, or pass configuration directly to `Frontal`. The SDK does not load `.env` files. See the root `.env.example` for local development conventions.

## Modules

See [the architecture guide](../../docs/ARCHITECTURE.md) and [service inventory](../../docs/SERVICES.md).

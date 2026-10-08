---
name: frontal-sdk-python
description: Guidance for adding or reviewing integrations using the Frontal Python SDK.
---

# Frontal Python SDK

The package-level client, shared core runtime, models, and resource methods are implemented. Resource methods are generated from `contracts/sdk-endpoints.json`; regenerate them with `python3 scripts/generate_resources.py` after contract changes. Follow the package structure and toolchain documented in this repository.

## Configuration

Use `Frontal.from_env()` to read `FRONTAL_API_KEY` and optional `FRONTAL_API_URL` from the process environment, or pass configuration directly to `Frontal`. The SDK does not load `.env` files. See the root `.env.example` for local development conventions.

## Modules

See [the architecture guide](../../docs/ARCHITECTURE.md) and [resource guide](../../docs/RESOURCES.md).

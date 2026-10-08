---
name: python-pydantic-httpx-contracts
description: Maintain Pydantic request/response models and contract-tested HTTPX resource methods in the Frontal Python SDK.
---

# Python Models and HTTPX Contracts

Use this skill when adding typed resource methods, changing model validation, or aligning behavior with Frontal API contracts.

- Check `contracts/sdk-endpoints.json` and the matching OpenAPI snapshot for method, path, and declared wire fields. Do not invent public operations or model fields.
- Put boundary models in `frontal_sdk/models` using the repository's Pydantic v2 conventions; keep resource methods hand-written in `frontal_sdk/resources`.
- Preserve wire aliases and serialization behavior. Avoid weakening validation to accept undocumented payload shapes.
- Use RESPX at the HTTPX layer for offline tests. Assert request construction, typed response parsing, validation failures, and API/network error mapping.
- Run `uv run python scripts/check_contracts.py`, Ruff, strict mypy, and focused pytest coverage; README snippets are executable in CI.

Keep `frontal_sdk/py.typed` and the supported Python versions intact.

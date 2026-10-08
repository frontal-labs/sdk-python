# Python SDK architecture

The repository builds one `frontal-sdk` distribution from the top-level `frontal_sdk/` package. The installed package contains the public client, shared runtime, transport boundary types, and typed API resources. Tests, documentation, examples, templates, and API contracts stay outside the runtime package.

## Package layout

```text
frontal_sdk/
├── __init__.py       # Stable package-level exports
├── client.py         # Unified Frontal client and resource ownership
├── core/             # Configuration, HTTP transport, errors, operations
├── models/           # JSON boundary and shared request/response values
├── resources/        # Typed methods grouped by API domain
└── py.typed          # PEP 561 marker for inline typing
```

`Frontal` owns one validated configuration and one shared HTTP transport. Each resource instance receives that transport and supplies operation-specific method signatures. The resource methods are generated from `contracts/sdk-endpoints.json`, which remains the source of truth for method and route shapes. `core/operation.py` renders path parameters, while `core/http.py` owns authentication, retries, error decoding, multipart, raw responses, and server-sent events.

## Request flow

`Application → Frontal → domain resource method → shared HttpClient → Frontal API`

## Models and contract boundaries

The SDK exposes JSON boundary aliases and shared types such as query mappings, multipart parts, and server events. The committed SDK endpoint inventory has method and path information but does not provide operation-specific request or response schemas for these endpoints. Resource payloads therefore use JSON types rather than guessed domain models. Add domain models when the API contracts define their shapes.

## Generation

Regenerate resource modules after updating the endpoint inventory:

```bash
python3 scripts/generate_resources.py
```

The generator rejects duplicate method names within a resource. Generated methods keep path arguments explicit, expose query and JSON body inputs where appropriate, and specialize streaming and binary operations.

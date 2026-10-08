# Python SDK architecture

The `frontal` distribution installs the `frontal_sdk` package. The package
contains the public sync and async clients, shared runtime, Pydantic models,
and service methods. Tests, documentation, examples, templates, and API
contracts stay outside the runtime package.

## Package layout

```text
frontal_sdk/
├── __init__.py       # Stable package-level exports
├── client.py         # Frontal and AsyncFrontal service ownership
├── core/             # Configuration, HTTP transports, errors, pagination
├── models/           # Pydantic request/response and shared boundary types
├── resources/        # Typed methods grouped by API domain
└── py.typed          # PEP 561 marker for inline typing
```

`Frontal` owns one validated configuration and an `httpx.Client`. `AsyncFrontal`
owns the matching `httpx.AsyncClient`. Both clients construct the same generic
service resources; their transport result types make synchronous calls return
JSON and asynchronous calls return awaitables. Event streams are synchronous
iterators or asynchronous iterators as appropriate.

`core/http.py` handles bearer authentication, `FRONTAL_ENV`, request IDs,
bounded retries for GET requests, Pydantic JSON validation, structured errors,
multipart uploads, raw bytes, and server-sent events. `core/pagination.py` and
`core/polling.py` provide sync and async cursor iteration and polling helpers.

## Request flow

```text
Application → Frontal or AsyncFrontal → service method → shared HTTPX transport → Frontal API
```

## Models and contract boundaries

Pydantic v2 models are available to callers through `APIModel`. The endpoint
inventory defines the current method and path surface, but most OpenAPI
operations do not define request or response schemas. Payloads therefore use a
validated JSON value boundary; the SDK avoids guessing service-specific field
shapes. `PageResult[T]` and `PaginationMeta` model cursor pagination where an
API response provides the documented pagination envelope.

The committed endpoint inventory and OpenAPI snapshots remain the source of
truth. Methods stay hand-written in their domain modules, and
`scripts/check_contracts.py` validates inventory coverage and API drift.

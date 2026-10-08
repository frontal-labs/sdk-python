# Python SDK architecture

The repository builds one `frontal-sdk` distribution from the top-level `frontal_sdk/` package. The installed package contains public Python APIs and service modules; repository documentation, tests, examples, and API contracts stay outside that package.

## Package layout

```text
frontal_sdk/
├── __init__.py       # Stable package-level public exports
├── client.py         # Unified Frontal client
├── api_types.py      # Public JSON boundary types
├── py.typed          # PEP 561 marker for inline typing
├── services/         # Shared client base and service-specific clients/catalogs
└── utils/            # Shared configuration, transport, errors, and operations
```

The `frontal_sdk` package is the installed distribution. Its root re-exports the stable public API, `client.py` owns unified client construction, `utils/` provides shared infrastructure, and `services/base.py` provides the shared typed client behavior used by service-specific clients and endpoint catalogs. Test fixtures and fakes belong in the repository's `tests/` tree unless a testing API is deliberately designed and supported as part of the SDK.

Keep Markdown guidance under `docs/` rather than inside import packages. Keep request and response models close to the service that owns them. Do not duplicate authentication, transport defaults, or retry policy across service modules.

## Repository layout

- `frontal_sdk/` — installable SDK package.
- `tests/` — unit and integration tests, kept out of runtime distributions.
- `contracts/` — shared OpenAPI snapshots, endpoint inventory, and this SDK's conformance reports.
- `docs/` — architecture, service inventory, developer, testing, and release guidance.
- `examples/` and `templates/` — Python integration examples and starter projects.

## Request flow

`Application → package-level Frontal client → typed service client → shared service and utility layers → Frontal API`

## Current implementation status

The package-level client, shared configuration and HTTP transport, typed service clients, endpoint catalogs, and initial local-server tests are implemented. Dedicated request/response models remain future work.

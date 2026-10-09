# Changelog

All notable changes to this SDK are recorded here.

<!-- towncrier release notes start -->

## 2.0.0 (2026-10-09)

### Breaking changes

- Rename inventory-backed methods to resource-oriented names and replace generic path parameters with semantic identifiers. See [the migration guide](docs/MIGRATION_2_0.md) for the full mapping.
- Distinguish omitted request bodies from JSON `null` and `{}`. Omitting `body` now sends no body.

### Features

- Add `FrontalError.transient` and `FrontalError.safe_to_retry` to separate temporary failures from safe replay.
- Add jitter to client-generated retry delays and enforce asynchronous polling deadlines.

### Bug fixes

- Preserve server-sent event IDs across events that omit a new ID.
- Retain details from non-standard JSON error responses and validate pagination limits.

## 1.0.0 (2026-10-08)

### Features

- Release the unified Python 1.0 SDK with synchronous and asynchronous clients, all 370 catalogued operations, typed AI text generation and embeddings, fluent agent and workflow builders, Pydantic v2 request models, offline HTTPX tests, and PyPI trusted publishing.
- Add sync and async AI tool registry helpers, plus agent configuration, approval predicate, and run completion polling helpers.

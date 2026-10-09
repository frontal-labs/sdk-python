# Changelog

All notable changes to this SDK are recorded here.

<!-- towncrier release notes start -->

## 1.0.0 (2026-10-09)

### Breaking changes

- Use resource-oriented method names and semantic path parameters.
- Distinguish omitted request bodies from JSON `null` and `{}`. Omitting `body` now sends no body.

### Features

- Provide synchronous and asynchronous clients, all 370 catalogued operations,
  typed AI helpers, and fluent agent and workflow builders.
- Add `FrontalError.transient` and `FrontalError.safe_to_retry` to separate temporary failures from safe replay.
- Add jitter to client-generated retry delays and enforce asynchronous polling deadlines.
- Add agent configuration, approval predicates, and run completion polling.

### Bug fixes

- Preserve server-sent event IDs across events that omit a new ID.
- Retain details from non-standard JSON error responses and validate pagination limits.

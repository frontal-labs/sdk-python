# Changelog

All notable changes to this SDK are recorded here.

<!-- towncrier release notes start -->

## [2.0.0](https://github.com/frontal-labs/sdk-python/compare/v1.0.0...v2.0.0) (2026-10-09)


### ⚠ BREAKING CHANGES

* **sdk:** redesign resource API and harden transport

### Features

* close remaining SDK parity gaps ([df0861c](https://github.com/frontal-labs/sdk-python/commit/df0861cb505b5f1d35f92c6c4ce3dfa7990e5264))
* complete typed AI and workflow service parity ([5b1f536](https://github.com/frontal-labs/sdk-python/commit/5b1f536d899bfc631f95d47eec5930ecedeea182))
* **devex:** add SDK agent skills and editor guidance ([#8](https://github.com/frontal-labs/sdk-python/issues/8)) ([5fa9e44](https://github.com/frontal-labs/sdk-python/commit/5fa9e44511eb6a12eb437e8e98678dbf8a0e6246))
* **functions:** add functions resource ([d0dd184](https://github.com/frontal-labs/sdk-python/commit/d0dd18471ae472f974cb04d74b031518804e7975))
* **functions:** add functions resource ([17b56b7](https://github.com/frontal-labs/sdk-python/commit/17b56b748607ea0b2771f1ab75e46e5c573eb4de))
* **sdk:** redesign resource API and harden transport ([c717829](https://github.com/frontal-labs/sdk-python/commit/c7178292dfec063b7b06db0682a3c5313fd2e32c))


### Bug Fixes

* **ci:** dispatch PyPI publishing after releases ([#7](https://github.com/frontal-labs/sdk-python/issues/7)) ([5f2756b](https://github.com/frontal-labs/sdk-python/commit/5f2756bf06bf740cf47f6b57c782c1d6cf9e5caf))
* **ci:** pin uv run environment behavior ([90d4dcc](https://github.com/frontal-labs/sdk-python/commit/90d4dcc46036c8a949cc44c8d4b6aa5b8f9161dd))
* **http:** stop retrying streams after yielding events ([0d9b812](https://github.com/frontal-labs/sdk-python/commit/0d9b8121d75f4bac7fa5f17d582d43d4cbfcecd5))
* **quality:** reduce Sonar complexity ([255d493](https://github.com/frontal-labs/sdk-python/commit/255d493ef4d439bc6a5fd5a821f46f3a7c64a5e6))
* **quality:** share event stream constants ([f02198b](https://github.com/frontal-labs/sdk-python/commit/f02198b4744006baed4b462e3a0549a7e1a0848e))
* validate API keys against Frontal format ([45e43b8](https://github.com/frontal-labs/sdk-python/commit/45e43b8565b70e4233be0544e46c61b18d56f94a))


### Documentation

* **sdk:** add runnable examples and expand integration guidance ([fed73b8](https://github.com/frontal-labs/sdk-python/commit/fed73b8fee31c9640cacc02610e39c6d9e2f3815))

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

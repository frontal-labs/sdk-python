# Python API contracts

The JSON and OpenAPI files here are shared Frontal API inputs.
`sdk-endpoints.json` records the SDK's service methods and paths, while
`coverage-floor.json` ratchets how many published snapshot operations the
inventory matches. Keep the public client hand-written and do not edit
upstream OpenAPI snapshots by hand.

`reports/conformance.json` and `reports/migration-matrix.md` describe the
implemented method and path coverage. Run `python scripts/check_contracts.py`
after changing the endpoint inventory or service methods.

The published `api.openapi.json` snapshot is a pinned upstream baseline
(`sha256` in `openapi/manifest.json`) that covers a subset of the API with a
different path vocabulary than the SDK implements, so the checker reports
inventory operations absent from the snapshot and snapshot operations outside
the inventory as informational drift, not failures. Update
`coverage-floor.json` when the matched baseline legitimately changes.

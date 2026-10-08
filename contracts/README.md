# Python API contracts

The JSON and OpenAPI files here are shared Frontal API inputs.
`sdk-endpoints.json` records the SDK's service methods and paths, while
`coverage-floor.json` records an existing coverage baseline. Keep the public
client hand-written and do not edit upstream OpenAPI snapshots by hand.

`reports/conformance.json` and `reports/migration-matrix.md` describe the
implemented method and path coverage. Run `python scripts/check_contracts.py`
after changing the endpoint inventory or service methods.

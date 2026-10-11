# Python SDK endpoint coverage

_Status: hand-written endpoint methods follow the committed SDK endpoint inventory._

| Metric | Value |
| --- | ---: |
| Implemented endpoint methods | 383 |
| Contract endpoint entries | 383 |
| Coverage | 100% |

Method and path coverage is complete for `contracts/sdk-endpoints.json`. Request and response payloads use a Pydantic-validated JSON boundary because the inventory does not include operation-specific payload schemas.

## Published OpenAPI snapshot conformance

The snapshots in `contracts/openapi/` are pinned upstream inputs (`sha256`
values in `contracts/openapi/manifest.json`) and are not edited in this
repository. `python scripts/check_contracts.py` reports how the endpoint
inventory lines up with them:

| Metric | api surface | ai surface |
| --- | ---: | ---: |
| Snapshot operations | 383 | 7 |
| Matched by the inventory | 142 | 7 |
| Inventory operations absent from the snapshot | 227 | 0 |
| Snapshot operations outside the inventory | 241 | 0 |

The published `api.openapi.json` baseline covers a subset of the API with a
different path vocabulary than the SDK implements (for example `/v1/integrations/...`
instead of the SDK's `/connectors/...`), so both gaps are expected drift, not
failures. The inventory remains the contract source for implemented methods,
and the matched baseline is ratcheted by `contracts/coverage-floor.json`.

# Service modules

Service clients and endpoint catalogs live in the matching package under `frontal_sdk/services/`. Each service package exports its `<Service>Client` and `<Service>Endpoint`. They inherit shared request dispatch, uploads, raw requests, and streaming from `frontal_sdk/services/base.py`; transport and endpoint descriptors live in `frontal_sdk/utils/`.

The service packages correspond to the endpoint domains in [`contracts/sdk-endpoints.json`](../contracts/sdk-endpoints.json):

- Agents
- AI
- Audit
- Auth
- Billing
- Blob
- Connectors
- Data
- Governance
- Lineage
- Observability
- Ontology
- Pipelines
- Sandbox
- Schedules
- Webhooks
- Workflows

The endpoint enums describe operations from the contract inventory. Clients currently expose generic dispatch through those typed endpoint enums; operation-specific request/response models and convenience methods have not been added. An endpoint in the contract inventory does not imply that the operation has a dedicated Python method. Add a test, API documentation, and a runnable example when adding one.

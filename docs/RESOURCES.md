# API resources

`Frontal` and `AsyncFrontal` expose the same service namespaces:

| Attribute | API domain |
| --- | --- |
| `ai` | AI generation and gateway operations |
| `agents` | Agent definitions and runs |
| `workflows` | Workflow definitions and executions |
| `audit`, `auth`, `billing` | Audit events, authentication, and billing |
| `blob`, `connectors`, `data` | Files, integrations, and data operations |
| `governance`, `lineage`, `observability` | Governance, lineage, and telemetry |
| `ontology`, `pipelines` | Ontology and pipelines operations |
| `schedules`, `webhooks` | Schedules and webhook operations |

## AI helpers

The AI resource includes validated helpers for common tasks. For example,
`generate_text()` returns a `GenerateTextResult`, while `stream_text()` yields
typed text, tool-call, finish, error, and done parts. `generate_object()` takes
a Pydantic model or schema and validates the generated JSON against it.

```python
from frontal_sdk import Frontal

with Frontal() as client:
    answer = client.ai.generate_text(
        {"model": "frontal-ai-fast", "prompt": "Summarize cursor pagination."}
    )
    print(answer.text)
```

`AsyncFrontal.ai` provides async counterparts. Consume its stream with
`async for` and await response-producing helpers.

## Agents and workflows

Definition builders validate inputs before sending them:

```python
from frontal_sdk import Frontal

with Frontal() as client:
    agent = (
        client.agents.define("Ticket triage")
        .description("Route incoming support tickets")
        .trigger("ticket.created")
        .can_read("tickets")
        .create()
    )
```

Use `client.agents.use(agent_id)` to message an agent, inspect its runs, poll
with `wait_for_completion()`, or watch a run as server events. Use
`client.workflows.define(name)` to add manual, schedule, event, or webhook
triggers and validated task steps. Create it with `.create()`, or publish it
immediately with `.activate()`. `client.workflows.use(workflow_id)` can trigger
an execution, list executions, and poll one to a terminal state. The same
accessors work with `AsyncFrontal`; await their results and use `async for` for
streams.

## Endpoint methods

Each service also exposes methods corresponding to the committed inventory.
For example:

```python
from frontal_sdk import Frontal

with Frontal() as client:
    agent = client.agents.get(id="agent_123")
    page = client.agents.list(query={"limit": 20})
```

The `agents` collection exposes concise `get(id=...)` and `list(query=...)`
methods, with runs and versions under `client.agents.runs` and
`client.agents.versions`. Other service namespaces continue to expose their
current resource-oriented operation names. Across them, use `query=` for query
parameters, `body=` for JSON writes, `parts=` for multipart uploads, and `data=`
with `content_type=` for raw request bodies. Streaming methods return
`ServerEvent` iterators; raw response-body methods return bytes.

Pydantic models cover shared and high-level boundaries. Raw operation payloads
use `JSONValue` where the OpenAPI snapshots do not define operation-specific
schemas. The endpoint inventory and OpenAPI snapshots remain authoritative;
the contract gate checks that endpoint methods do not drift. Run
`python scripts/check_contracts.py` after changing inventory-backed methods.

The SDK uses resource-oriented names and semantic path arguments.

If you inject an `httpx.Client` or `httpx.AsyncClient`, set its timeout on that
HTTPX instance. The SDK uses the injected instance as-is and leaves closing it
to your application:

```python
import httpx
from frontal_sdk import Frontal

http = httpx.Client(timeout=httpx.Timeout(10.0, connect=2.0))
with Frontal(http_client=http) as client:
    agents = client.agents.list()
http.close()
```

## Pagination and errors

The endpoint inventory does not assign a response model to every collection.
Validate the documented page envelope at the call site, then use the shared
cursor helper:

```python
from frontal_sdk import Frontal, PageResult, RateLimitError, paginate
from frontal_sdk.models import JSONValue

with Frontal() as client:

    def fetch_agents(query):
        response = client.agents.list(query=query)
        return PageResult[dict[str, JSONValue]].model_validate(response)

    try:
        agent_rows = list(paginate(fetch_agents, query={"limit": 50}))
    except RateLimitError as error:
        print(error.request_id, error.retry_after)
```

Each fetch callback receives the original query plus the cursor returned by the
prior page. Configure `timeout` on the client as well as on polling helpers: a
polling deadline cannot interrupt a blocking synchronous fetch.

## Request bodies and retry safety

Write methods distinguish an omitted body from JSON values. Omitting `body`
sends no request body; `body=None` sends JSON `null`, and `body={}` sends an
empty JSON object. API errors expose `transient` for temporary failures and
`safe_to_retry` for operations that can be replayed safely. A transient error
from a write may still represent an operation the server accepted, so inspect
`safe_to_retry` before replaying it.

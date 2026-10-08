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
| `ontology`, `pipelines`, `sandbox` | Ontology, pipelines, and sandbox operations |
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

## Raw endpoint methods

Each service also exposes methods corresponding to the committed inventory.
For example:

```python
from frontal_sdk import Frontal

with Frontal() as client:
    agent = client.agents.get_agents_by_param_1("agent_123")
    page = client.agents.get_agents(query={"limit": 20})
```

Raw method names include the HTTP verb and route segments. Since the inventory
does not preserve path parameter names, placeholders appear as `param_1`,
`param_2`, and so on in route order. Use `query=` for query parameters,
`body=` for JSON writes, `parts=` for multipart uploads, and `data=` with
`content_type=` for raw request bodies. Raw streaming methods return
`ServerEvent` iterators; raw response-body methods return bytes.

Pydantic models cover shared and high-level boundaries. Raw operation payloads
use `JSONValue` where the OpenAPI snapshots do not define operation-specific
schemas. The endpoint inventory and OpenAPI snapshots remain authoritative;
the contract gate checks that endpoint methods do not drift. Run
`python scripts/check_contracts.py` after changing inventory-backed methods.

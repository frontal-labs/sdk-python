# Getting started

Install the package, set `FRONTAL_API_KEY`, and make your first request in
under five minutes.

## Install

Python 3.9–3.12 is supported.

```bash
pip install frontal
# or
uv add frontal
```

## Configure

The client reads its API key from `FRONTAL_API_KEY`. The base URL,
environment header, and debug logging read `FRONTAL_API_URL`,
`FRONTAL_ENV`, and `FRONTAL_DEBUG` when their constructor arguments are
omitted. The SDK does not load `.env` files.

```bash
export FRONTAL_API_KEY="frt_..."
```

## Hello world

```python
from frontal_sdk import Frontal

with Frontal() as client:
    result = client.ai.generate_text(
        {"model": "frontal-ai-fast", "prompt": "Say hello."}
    )
    print(result.text)
```

The async client exposes the same services and operation methods:

```python
import asyncio

from frontal_sdk import AsyncFrontal


async def main() -> None:
    async with AsyncFrontal() as client:
        result = await client.ai.generate_text(
            {"model": "frontal-ai-fast", "prompt": "Say hello."}
        )
        print(result.text)


asyncio.run(main())
```

## Define an agent

Builders validate inputs before anything is sent:

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

Message it, poll a run, or watch run events:

```python
from frontal_sdk import AgentExecution, Frontal

with Frontal() as client:
    accessor = client.agents.use("agt_ticket_triager")
    run = AgentExecution.model_validate(
        accessor.message("support.ticket.created", {"ticketId": "t_987"})
    )
    final = accessor.wait_for_completion(run.id)
    for event in accessor.watch(run.id):
        print(event.event, event.data)
```

## Stream text

`stream_text()` yields typed parts — text deltas, tool calls, a finish
part with usage, error parts, and a terminal done part:

```python
with Frontal() as client:
    for part in client.ai.stream_text(
        {"model": "frontal-ai-fast", "prompt": "Count to three."}
    ):
        if part.type == "text":
            print(part.text, end="", flush=True)
        elif part.type == "finish":
            print(f"\n[finished: {part.finish_reason}]")
```

## Handle errors

Every API failure raises a `FrontalError` subclass carrying the error
`code`, `request_id`, `status_code`, a `transient` flag, an explicit
`safe_to_retry` signal, and — when the SDK knows one — a human-readable
`fix` hint:

```python
from frontal_sdk import Frontal, FrontalError, RateLimitError, ValidationError

with Frontal() as client:
    try:
        client.agents.list(query={"limit": 50})
    except RateLimitError as error:
        print(f"Rate limited; retry after {error.retry_after}s")
    except ValidationError as error:
        for field in error.fields:
            print(f"  - {field.field}: {field.message}")
    except FrontalError as error:
        print(f"Request failed [{error.code}]: {error}")
        if error.fix is not None:
            print(f"Hint: {error.fix}")
```

A transient error from a write may still represent an operation the
server accepted, so inspect `safe_to_retry` before replaying it.

## Next steps

- [API resources](RESOURCES.md) — AI helpers, builders, endpoint methods,
  pagination, and retry safety.
- [Functions API](FUNCTIONS.md) — function definitions, invocations, and
  executions.
- [Architecture](ARCHITECTURE.md) — package layout, config, transport,
  retries, and streaming semantics.
- [Runnable examples](../examples/README.md) — offline scripts covering
  agents, functions, workflows, streaming, and error handling.
- [Testing](TESTING.md) — offline RESPX coverage and runnable documentation.

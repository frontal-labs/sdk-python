# Python examples

These scripts use the public Python client and do not load `.env` files
automatically. Set `FRONTAL_API_KEY` in your shell before running an example.
Each script closes its HTTPX client when finished.

| File | Demonstrates |
| --- | --- |
| [`quickstart.py`](./quickstart.py) | Synchronous text generation |
| [`async_quickstart.py`](./async_quickstart.py) | Async text generation with `AsyncFrontal` |
| [`define_agent.py`](./define_agent.py) | Validated agent builder and scoped access |
| [`create_function.py`](./create_function.py) | Function definition and invocation |
| [`create_workflow.py`](./create_workflow.py) | Workflow creation and triggering an execution |

Run scripts from the repository root after installing the development extra:

```bash
uv sync --extra dev
uv run python examples/quickstart.py
uv run python examples/async_quickstart.py
uv run python examples/define_agent.py
uv run python examples/create_function.py
uv run python examples/create_workflow.py
```

The examples are also exercised offline by `tests/test_examples.py`, which
intercepts HTTPX requests with RESPX. See the [integration guide](./SDKS_GUIDE.md)
for client setup, raw endpoint methods, and links to the resource reference.

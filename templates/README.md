# Python SDK templates

These starter projects target common Python application setups. Every template uses the Python SDK directly and keeps its entry point and configuration in Python project files.

| Template | Best for | Entry point |
| --- | --- | --- |
| [`cli/`](./cli/) | A reusable command line application | `frontal-cli` |
| [`batch-job/`](./batch-job/) | Processing a file of API identifiers | `frontal-batch` |
| [`async-client/`](./async-client/) | Concurrent requests with the native asynchronous client | `frontal-async` |

Each directory is a standalone Python project with a `pyproject.toml` and its
own setup guide. After `frontal` 1.0.0 is available on PyPI, install the SDK
dependency and the template's command with:

```bash
cd templates/cli
uv sync
uv run frontal-cli --help
```

To develop against the SDK source in this checkout, run `uv add --editable ../..`
from the chosen template directory, then use `uv sync`. This adds the local SDK
checkout as an editable dependency. Set `FRONTAL_API_KEY` before making API
requests. Set `FRONTAL_API_URL` to target a non-default API URL. Installation
does not call the API, and credentials do not belong in template files.

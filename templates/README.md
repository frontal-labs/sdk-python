# Python SDK templates

These starter projects target common Python application setups. Every template uses the Python SDK directly and keeps its entry point and configuration in Python project files.

| Template | Best for | Entry point |
| --- | --- | --- |
| [`cli/`](./cli/) | A reusable command line application | `frontal-cli` |
| [`batch-job/`](./batch-job/) | Processing a file of API identifiers | `frontal-batch` |
| [`async-client/`](./async-client/) | Calling the synchronous SDK from an asyncio application | `frontal-async` |

Each directory is a standalone Python project with a `pyproject.toml` and its own setup guide. From a template directory in this repository, install the local SDK and the template with:

```bash
python -m pip install -e ../..
python -m pip install -e .
```

Set `FRONTAL_API_KEY` before running a template. Set `FRONTAL_API_URL` when targeting a non-default API URL. The starter projects do not include credentials or call the API during installation.

# CLI template

A small, installable command line app using Python's `argparse` and the Frontal
SDK. The `frontal-cli` entry point exposes an AI gateway health check, an agent
list request, and a lookup by agent ID. It closes its HTTP client after each
command.

## Install

From this directory:

```bash
uv sync
```

`uv sync` installs `frontal>=1.0.0` from PyPI. To use the SDK source in this
repository checkout, follow the editable dependency instructions in
[`templates/README.md`](../README.md).

Set `FRONTAL_API_KEY` in your shell. Then run:

```bash
uv run frontal-cli health
uv run frontal-cli agents
uv run frontal-cli agent agent_123
```

Use `FRONTAL_API_URL` to override the default API URL. The CLI prints API results as JSON and sends request errors to stderr.

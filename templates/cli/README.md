# CLI template

A small, installable command line app using only Python's `argparse` plus the Frontal SDK. The `frontal-cli` entry point exposes a health check, an agent list request, and a lookup by agent ID.

## Install

From this directory:

```bash
uv sync
```

Set `FRONTAL_API_KEY` in your shell. Then run:

```bash
uv run frontal-cli health
uv run frontal-cli agents
uv run frontal-cli agent agent_123
```

Use `FRONTAL_API_URL` to override the default API URL. The CLI prints API results as JSON and sends request errors to stderr.

# Batch job template

This template reads one agent ID per line, looks up each record with the SDK, and writes JSON Lines output. It logs failures to stderr, keeps processing later IDs, and exits with status `1` if any lookup failed.

## Install

From this directory:

```bash
uv sync
```

Create an input file and set `FRONTAL_API_KEY`:

```text
agent_123
agent_456
```

Run the job and capture its output:

```bash
uv run frontal-batch agent-ids.txt > results.jsonl
```

Set `FRONTAL_API_URL` when using a non-default API URL. Keep credentials in the process environment or your job runner's secret store; do not add them to the input file.

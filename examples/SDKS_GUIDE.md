# Python SDK integration guide

Install the SDK from the repository root during development:

```bash
uv sync --extra dev
```

Set `FRONTAL_API_KEY` in the environment, then use the unified client and typed resource methods:

```python
from frontal_sdk import Frontal

client = Frontal.from_env()
health = client.ai.get_health()
agents = client.agents.get_agents(query={"limit": 20})
```

Path parameters are required positional arguments, query parameters use `query=`, and write requests accept a JSON `body=`. See [`docs/RESOURCES.md`](../docs/RESOURCES.md) for multipart, raw response, and streaming methods.

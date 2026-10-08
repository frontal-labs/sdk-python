# API resources

The unified `Frontal` client exposes one typed resource per endpoint domain. For example:

```python
from frontal_sdk import Frontal

client = Frontal.from_env()
agent = client.agents.get_agents_by_param_1("agent_123")
health = client.ai.get_health()
```

The domains and method inventory are generated from [`contracts/sdk-endpoints.json`](../contracts/sdk-endpoints.json). Resource method names preserve the HTTP verb and route segments. Placeholder values are exposed as `param_1`, `param_2`, and so on in route order because the shared endpoint inventory does not provide parameter names.

JSON methods accept `query=` and write methods accept `body=`. Multipart uploads take `parts=` and raw body operations accept `data=` and `content_type=`. Streaming endpoints return an iterator of `ServerEvent`; raw endpoints return `bytes`.

Regenerate resource methods with `python3 scripts/generate_resources.py`. Update the contract inventory first so generated methods and conformance data stay aligned.

# Functions API

`Frontal` and `AsyncFrontal` expose the Functions service as
`client.functions`. It uses the shared client configuration and HTTPX transport:
the default API URL is `https://api.frontal.dev/v1`, the default timeout is 30
seconds, and the default retry count is three. Pass `api_key`, `base_url`,
`timeout`, and `max_retries` to either client to override those values. The API
key is sent as Bearer authentication.

## Create and invoke

Function definitions require `name`, `runtime` (`nodejs20`, `nodejs22`, or
`python311`), and `entrypoint`. Optional fields include `description`, `source`,
`input_schema`, `output_schema`, `dependencies`, `env_vars`, `secrets`,
`memory` in MB, `timeout` in seconds, and `permissions` with `ontology` and
`actions` string arrays. Schema and invocation data accept arbitrary nested JSON
objects.

```python
from frontal_sdk import (
    Frontal,
    FunctionInvocationInput,
    FunctionInvocationResult,
    FunctionResource,
)

with Frontal(api_key="frt_your_api_key") as client:
    created = (
        client.functions.define("hello-world")
        .runtime("nodejs22")
        .entrypoint("index.handler")
        .input_schema({"type": "object", "properties": {"name": {"type": "string"}}})
        .create()
    )
    function = FunctionResource.model_validate(created)
    raw_result = client.functions.executions.invoke(
        FunctionInvocationInput(
            function_id=function.id,
            input={"name": "World", "metadata": {"requestTag": "sample"}},
        )
    )
    result = FunctionInvocationResult.model_validate(raw_result)
    print(result.result)
```

The same resources work with `AsyncFrontal`; await calls such as
`client.functions.executions.invoke(...)`. `client.functions.versions` provides
`list`, `get`, and `publish`; `client.functions.deployments` provides `deploy`
and `status`; `client.functions.executions` provides `invoke`, `invoke_async`,
`get`, `get_result`, `list`, and `cancel`.

List methods accept the API's cursor names through `query=`, for example:
`client.functions.list(query={"cursor": "next", "limit": 25})`. Execution
filters use `functionId` and `status` in the query mapping.

## Errors

Functions requests use the shared typed SDK errors. HTTP 400 and 422 responses
raise `ValidationError`; 401 and 403 raise `AuthenticationError`; 404 raises
`NotFoundError`; 409 raises `ConflictError`; 429 raises `RateLimitError`; and
5xx responses raise `ServerError`. Connection and timeout failures raise
`NetworkError` and `TimeoutError`. Errors expose `status_code`, `code`,
`request_id`, `details`, `transient`, and `safe_to_retry`; rate limit errors
also expose `retry_after`. The SDK does not automatically retry function write
requests when replay could repeat an accepted operation.

The Functions routes are recorded in `contracts/sdk-endpoints.json` from the
TypeScript Functions client and its package tests. The currently checked-in
OpenAPI snapshots do not contain these routes.

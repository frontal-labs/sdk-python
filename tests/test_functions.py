"""Offline tests for the Frontal Functions resources and models."""

from __future__ import annotations

import json
from collections.abc import Iterator

import httpx
import pytest
import respx
from frontal_sdk import (
    AsyncFrontal,
    Frontal,
    FunctionDefinition,
    FunctionExecutionListResponse,
    FunctionInvocationInput,
    FunctionInvocationResult,
    FunctionListResponse,
    NotFoundError,
    ValidationError,
)

API_URL = "https://api.frontal.dev/v1"


@pytest.fixture
def respx_mock() -> Iterator[respx.Router]:
    with respx.mock(assert_all_called=False) as router:
        yield router


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


def _mock_operation(
    router: respx.Router, method: str, path: str, *, status_code: int = 200
) -> respx.Route:
    return getattr(router, method.lower())(f"{API_URL}{path}").mock(
        return_value=(
            httpx.Response(status_code)
            if status_code == 204
            else httpx.Response(status_code, json={"ok": True})
        )
    )


def _definition() -> FunctionDefinition:
    return FunctionDefinition(
        name="nested-json",
        runtime="python311",
        entrypoint="handler.main",
        input_schema={
            "type": "object",
            "properties": {
                "payload": {"type": "object", "x-schema-meta": {"custom": True}}
            },
            "x-vendor-field": {"keep": [1, {"mixedCase": "preserved"}]},
        },
    )


def test_functions_operations_paths_queries_and_bodies(
    respx_mock: respx.Router,
) -> None:
    expected = [
        ("POST", "/functions"),
        ("GET", "/functions"),
        ("GET", "/functions/fn%2Fone"),
        ("PATCH", "/functions/fn%2Fone"),
        ("DELETE", "/functions/fn%2Fone"),
        ("GET", "/functions/fn%2Fone/versions"),
        ("GET", "/functions/fn%2Fone/versions/3"),
        ("POST", "/functions/fn%2Fone/versions/3/publish"),
        ("POST", "/functions/fn%2Fone/versions/3/deploy"),
        ("GET", "/functions/fn%2Fone/versions/3/deployment/status"),
        ("POST", "/functions/invoke"),
        ("POST", "/functions/invoke-async"),
        ("GET", "/functions/executions/exec%2Fone"),
        ("GET", "/functions/executions/exec%2Fone/result"),
        ("GET", "/functions/executions"),
        ("POST", "/functions/executions/exec%2Fone/cancel"),
    ]
    routes = {
        (method, path): _mock_operation(
            respx_mock,
            method,
            path,
            status_code=204 if method == "DELETE" else 200,
        )
        for method, path in expected
    }
    client = Frontal("frt_local_key", max_retries=0)
    definition = _definition()
    invocation = FunctionInvocationInput(
        function_id="fn/one",
        version=3,
        input={"query": {"deepKey": ["value", {"custom_key": 17}]}},
    )

    client.functions.create(definition)
    client.functions.list(query={"cursor": "page-2", "limit": 12})
    client.functions.get(id="fn/one")
    client.functions.update(id="fn/one", definition=definition)
    client.functions.delete(id="fn/one")
    client.functions.versions.list(
        function_id="fn/one", query={"cursor": "versions-2", "limit": 8}
    )
    client.functions.versions.get("fn/one", 3)
    client.functions.versions.publish("fn/one", 3)
    client.functions.deployments.deploy("fn/one", 3)
    client.functions.deployments.status("fn/one", 3)
    client.functions.executions.invoke(invocation)
    client.functions.executions.invoke_async(invocation)
    client.functions.executions.get("exec/one")
    client.functions.executions.get_result("exec/one")
    client.functions.executions.list(
        query={
            "cursor": "exec-2",
            "limit": 5,
            "functionId": "fn/one",
            "status": "failed",
        }
    )
    client.functions.executions.cancel("exec/one")

    for (method, path), route in routes.items():
        assert route.called, (method, path)
        request = route.calls.last.request
        assert request.method == method
        assert request.url.raw_path.split(b"?", 1)[0] == ("/v1" + path).encode()
        assert request.headers["authorization"] == "Bearer frt_local_key"

    assert dict(routes[("GET", "/functions")].calls.last.request.url.params) == {
        "cursor": "page-2",
        "limit": "12",
    }
    assert dict(
        routes[("GET", "/functions/fn%2Fone/versions")].calls.last.request.url.params
    ) == {
        "cursor": "versions-2",
        "limit": "8",
    }
    assert dict(
        routes[("GET", "/functions/executions")].calls.last.request.url.params
    ) == {
        "cursor": "exec-2",
        "limit": "5",
        "functionId": "fn/one",
        "status": "failed",
    }

    definition_body = json.loads(
        routes[("POST", "/functions")].calls.last.request.content
    )
    assert definition_body["inputSchema"] == definition.input_schema
    assert "input_schema" not in definition_body
    assert "description" not in definition_body
    assert definition_body["inputSchema"]["x-vendor-field"]["keep"][1] == {
        "mixedCase": "preserved"
    }
    assert json.loads(
        routes[("POST", "/functions/invoke")].calls.last.request.content
    ) == {
        "functionId": "fn/one",
        "version": 3,
        "input": {"query": {"deepKey": ["value", {"custom_key": 17}]}},
    }
    assert json.loads(
        routes[("POST", "/functions/invoke-async")].calls.last.request.content
    ) == json.loads(routes[("POST", "/functions/invoke")].calls.last.request.content)
    for method_path in (
        ("POST", "/functions/fn%2Fone/versions/3/publish"),
        ("POST", "/functions/fn%2Fone/versions/3/deploy"),
        ("POST", "/functions/executions/exec%2Fone/cancel"),
    ):
        assert json.loads(routes[method_path].calls.last.request.content) == {}
    client.close()


def test_functions_models_validate_pages_and_keep_nested_json() -> None:
    function_page = FunctionListResponse.model_validate(
        {
            "functions": [
                {
                    "id": "fn_1",
                    "name": "echo",
                    "runtime": "nodejs22",
                    "entrypoint": "index.handler",
                    "status": "active",
                    "version": 2,
                    "latestVersion": 2,
                    "createdAt": "2026-10-09T12:00:00Z",
                    "updatedAt": "2026-10-09T12:01:00Z",
                }
            ],
            "pagination": {"cursor": "next", "hasMore": True},
        }
    )
    execution_page = FunctionExecutionListResponse.model_validate(
        {
            "executions": [
                {
                    "id": "exec_1",
                    "functionId": "fn_1",
                    "version": 2,
                    "status": "active",
                    "input": {"arbitrary": {"deep": [1, {"CamelKey": True}]}},
                }
            ],
            "pagination": {"hasMore": False},
        }
    )
    result = FunctionInvocationResult.model_validate(
        {
            "executionId": "exec_1",
            "result": {"output": {"strange_JSON_key": {"values": [1, 2]}}},
            "status": "active",
        }
    )

    assert function_page.functions[0].latest_version == 2
    assert function_page.pagination.has_more is True
    assert execution_page.executions[0].input == {
        "arbitrary": {"deep": [1, {"CamelKey": True}]}
    }
    assert result.model_dump(mode="json", by_alias=True)["result"] == {
        "output": {"strange_JSON_key": {"values": [1, 2]}}
    }


def test_function_definition_requires_runtime_and_entrypoint() -> None:
    with pytest.raises(ValueError):
        FunctionDefinition.model_validate({"name": "incomplete"})


def test_functions_use_shared_base_url_configuration(respx_mock: respx.Router) -> None:
    route = respx_mock.post("https://functions.example.test/api/functions/invoke").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )
    client = Frontal(
        "frt_local_key",
        base_url="https://functions.example.test/api",
        timeout=12.0,
        max_retries=0,
    )
    client.functions.executions.invoke({"functionId": "fn_1", "input": {}})
    assert route.called
    assert route.calls.last.request.url.host == "functions.example.test"
    assert route.calls.last.request.url.path == "/api/functions/invoke"
    client.close()


def test_functions_api_errors_use_shared_error_mapping(
    respx_mock: respx.Router,
) -> None:
    respx_mock.get(f"{API_URL}/functions/missing").mock(
        return_value=httpx.Response(404, json={"message": "function not found"})
    )
    respx_mock.post(f"{API_URL}/functions").mock(
        return_value=httpx.Response(422, json={"message": "invalid function"})
    )
    client = Frontal("frt_local_key", max_retries=0)

    with pytest.raises(NotFoundError, match="function not found"):
        client.functions.get("missing")
    with pytest.raises(ValidationError, match="invalid function"):
        client.functions.create(_definition())
    client.close()


@pytest.mark.anyio
async def test_async_functions_share_routes_and_json_serialization(
    respx_mock: respx.Router,
) -> None:
    route = respx_mock.post(f"{API_URL}/functions/invoke-async").mock(
        return_value=httpx.Response(202, json={"executionId": "exec_1"})
    )
    async with AsyncFrontal("frt_local_key", max_retries=0) as client:
        response = await client.functions.executions.invoke_async(
            FunctionInvocationInput(
                function_id="fn_1", input={"nested": {"PascalKey": [1, 2]}}
            )
        )

    assert response == {"executionId": "exec_1"}
    assert json.loads(route.calls.last.request.content) == {
        "functionId": "fn_1",
        "input": {"nested": {"PascalKey": [1, 2]}},
    }

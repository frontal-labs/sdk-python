"""HTTPX transport tests using RESPX; no API backend is required."""

from __future__ import annotations

import json
from collections.abc import Iterator
from typing import Any

import httpx
import pytest
import respx
from frontal_sdk import (
    APIModel,
    AsyncFrontal,
    AuthenticationError,
    Frontal,
    FrontalError,
    MultipartPart,
    PageResult,
    RateLimitError,
    ServerEvent,
    ValidationError,
    async_paginate,
    async_poll_until,
    paginate,
    poll_until,
)
from frontal_sdk.core import ClientConfig, HttpClient, Operation
from pydantic import Field

API_URL = "https://api.frontal.dev/v1"


@pytest.fixture
def respx_mock() -> Iterator[respx.Router]:
    with respx.mock(assert_all_called=False) as router:
        yield router


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


class CreateAgent(APIModel):
    display_name: str = Field(alias="displayName")


def test_sync_request_auth_query_request_id_and_encoded_path(
    respx_mock: respx.Router,
) -> None:
    route = respx_mock.get(
        f"{API_URL}/agents/agent%2Fone", params={"include_runs": "True"}
    ).mock(return_value=httpx.Response(200, json={"ok": True}))

    client = Frontal("frt_local_key", max_retries=0)
    response = client.agents.get_agents_by_param_1(
        "agent/one", query={"include_runs": True}
    )

    request = route.calls.last.request
    assert response == {"ok": True}
    assert request.headers["authorization"] == "Bearer frt_local_key"
    assert request.headers["x-frontal-environment"] == "production"
    assert request.headers["x-request-id"]
    assert request.url.raw_path.split(b"?", 1)[0] == b"/v1/agents/agent%2Fone"
    assert request.url.params["include_runs"] == "True"
    client.close()


def test_pydantic_request_model_serializes_aliases(respx_mock: respx.Router) -> None:
    route = respx_mock.post(f"{API_URL}/agents").mock(
        return_value=httpx.Response(201, json={"id": "agent_1"})
    )
    client = Frontal("frt_local_key", max_retries=0)

    response = client.agents.post_agents(body=CreateAgent(display_name="sample"))

    assert response == {"id": "agent_1"}
    assert json.loads(route.calls.last.request.content) == {"displayName": "sample"}
    client.close()


def test_sync_get_retries_transient_server_errors(respx_mock: respx.Router) -> None:
    route = respx_mock.get(f"{API_URL}/agents").mock(
        side_effect=[
            httpx.Response(503),
            httpx.Response(200, json={"data": []}),
        ]
    )
    client = Frontal("frt_local_key", max_retries=1)

    assert client.agents.get_agents() == {"data": []}
    assert route.call_count == 2
    client.close()


@pytest.mark.parametrize(
    ("status", "error_type"),
    [(401, AuthenticationError), (422, ValidationError)],
)
def test_sync_error_categories_include_request_id(
    respx_mock: respx.Router,
    status: int,
    error_type: type[FrontalError],
) -> None:
    respx_mock.get(f"{API_URL}/agents").mock(
        return_value=httpx.Response(
            status,
            json={"code": "BAD_REQUEST", "message": "rejected"},
            headers={"X-Request-Id": "req_123"},
        )
    )
    client = Frontal("frt_local_key", max_retries=0)

    with pytest.raises(error_type) as raised:
        client.agents.get_agents()

    assert raised.value.status_code == status
    assert raised.value.request_id == "req_123"
    assert raised.value.retryable is False
    client.close()


def test_rate_limit_error_parses_retry_after(respx_mock: respx.Router) -> None:
    respx_mock.get(f"{API_URL}/agents").mock(
        return_value=httpx.Response(
            429,
            json={"code": "RATE_LIMITED", "message": "slow down"},
            headers={"Retry-After": "10"},
        )
    )
    client = Frontal("frt_local_key", max_retries=0)

    with pytest.raises(RateLimitError) as raised:
        client.agents.get_agents()

    assert raised.value.retryable is True
    assert raised.value.retry_after == 5.0
    client.close()


def test_multipart_and_raw_response(respx_mock: respx.Router) -> None:
    upload = respx_mock.post(f"{API_URL}/blob/object/reports/report.txt").mock(
        return_value=httpx.Response(200, json={"uploaded": True})
    )
    download = respx_mock.get(f"{API_URL}/blob/object/reports/report.txt").mock(
        return_value=httpx.Response(200, content=b"file contents")
    )
    client = Frontal("frt_local_key", max_retries=0)

    result = client.blob.upload_blob_object_by_param_1_by_param_2(
        "reports",
        "report.txt",
        [
            MultipartPart(
                "file",
                b"file contents",
                filename="report.txt",
                content_type="text/plain",
            )
        ],
        fields={"cacheControl": "3600"},
    )
    with HttpClient(ClientConfig("frt_local_key", max_retries=0)) as http:
        raw = http.request_bytes(
            Operation("GETRAW", "/blob/object/{param}/{param}"),
            path_params=("reports", "report.txt"),
        )

    assert result == {"uploaded": True}
    assert (
        "multipart/form-data; boundary="
        in upload.calls.last.request.headers["content-type"]
    )
    assert b"file contents" in upload.calls.last.request.content
    assert b"cacheControl" in upload.calls.last.request.content
    assert raw == b"file contents"
    assert download.called
    client.close()


def test_sync_sse_stream(respx_mock: respx.Router) -> None:
    route = respx_mock.get(f"{API_URL}/agents/runs/run_1/stream").mock(
        return_value=httpx.Response(
            200,
            headers={"Content-Type": "text/event-stream"},
            content=b'event: state\nid: evt_1\ndata: {"ready":true}\n\n',
        )
    )
    client = Frontal("frt_local_key", max_retries=0)

    events = list(client.agents.stream_agents_runs_by_param_1_stream("run_1"))

    assert [(item.event, item.id, item.data) for item in events] == [
        ("state", "evt_1", {"ready": True})
    ]
    assert route.called
    client.close()


@pytest.mark.anyio
async def test_async_request_and_retry(respx_mock: respx.Router) -> None:
    route = respx_mock.get(f"{API_URL}/health").mock(
        side_effect=[httpx.Response(503), httpx.Response(200, json={"ok": True})]
    )
    async with AsyncFrontal("frt_local_key", max_retries=1) as client:
        assert await client.ai.get_health() == {"ok": True}
    assert route.call_count == 2


@pytest.mark.anyio
async def test_async_error_mapping_and_sse(respx_mock: respx.Router) -> None:
    respx_mock.get(f"{API_URL}/agents").mock(
        return_value=httpx.Response(
            401,
            json={"code": "INVALID_API_KEY", "message": "denied"},
            headers={"X-Request-Id": "req_async"},
        )
    )
    stream_route = respx_mock.get(f"{API_URL}/agents/runs/run_2/stream").mock(
        return_value=httpx.Response(
            200,
            headers={"Content-Type": "text/event-stream"},
            content=b'data: {"step":1}\n\n',
        )
    )
    async with AsyncFrontal("frt_local_key", max_retries=0) as client:
        with pytest.raises(AuthenticationError) as raised:
            await client.agents.get_agents()
        events = [
            event
            async for event in client.agents.stream_agents_runs_by_param_1_stream(
                "run_2"
            )
        ]

    assert raised.value.request_id == "req_async"
    assert events == [ServerEvent("message", {"step": 1}, None)]
    assert stream_route.called


def test_sync_pagination_and_polling() -> None:
    calls: list[dict[str, Any]] = []

    def fetch(query: Any) -> PageResult[str]:
        calls.append(dict(query))
        cursor = query.get("cursor")
        return PageResult[str].model_validate(
            {
                "data": ["second"] if cursor else ["first"],
                "pagination": {
                    "cursor": "next" if not cursor else None,
                    "hasMore": not bool(cursor),
                },
            }
        )

    assert list(paginate(fetch, query={"limit": 1})) == ["first", "second"]
    assert calls == [{"limit": 1}, {"limit": 1, "cursor": "next"}]
    assert poll_until(lambda: "ready", interval=0.001, timeout=0.1) == "ready"


@pytest.mark.anyio
async def test_async_pagination_and_polling() -> None:
    async def fetch(query: Any) -> PageResult[int]:
        cursor = query.get("cursor")
        return PageResult[int].model_validate(
            {
                "data": [2] if cursor else [1],
                "pagination": {
                    "cursor": "next" if not cursor else None,
                    "hasMore": not bool(cursor),
                },
            }
        )

    items = [item async for item in async_paginate(fetch)]
    polled = await async_poll_until(lambda: _ready_value(), interval=0.001, timeout=0.1)
    assert items == [1, 2]
    assert polled == "ready"


async def _ready_value() -> str:
    return "ready"

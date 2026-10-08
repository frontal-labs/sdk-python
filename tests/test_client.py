"""HTTPX transport tests using RESPX; no API backend is required."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator, Iterator
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
    GenerateImageResult,
    GenerateObjectResult,
    GenerateTextResult,
    MultipartPart,
    NetworkError,
    PageResult,
    RateLimitError,
    ServerEvent,
    ValidationError,
    async_paginate,
    async_poll_until,
    paginate,
    poll_until,
    tool,
)
from frontal_sdk.core import ClientConfig, HttpClient, Operation
from pydantic import Field

API_URL = "https://api.frontal.dev/v1"


def _sse_response(events: list[object]) -> bytes:
    return b"".join(f"data: {json.dumps(event)}\n\n".encode() for event in events)


class _InterruptedSyncSSE(httpx.SyncByteStream):
    def __iter__(self) -> Iterator[bytes]:
        yield b'data: {"step":1}\n\n'
        raise httpx.ReadError("stream disconnected")

    def close(self) -> None:
        pass


class _InterruptedAsyncSSE(httpx.AsyncByteStream):
    def __aiter__(self) -> AsyncIterator[bytes]:
        return self._chunks()

    async def _chunks(self) -> AsyncIterator[bytes]:
        yield b'data: {"step":1}\n\n'
        raise httpx.ReadError("stream disconnected")

    async def aclose(self) -> None:
        pass


@pytest.mark.parametrize("api_key", ["plain-key", "frt_", "frt_abcd", "frt_bad.key"])
def test_client_rejects_malformed_api_key(api_key: str) -> None:
    with pytest.raises(ValueError, match="api_key must start with 'frt_'"):
        Frontal(api_key)


@pytest.fixture
def respx_mock() -> Iterator[respx.Router]:
    with respx.mock(assert_all_called=False) as router:
        yield router


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


class CreateAgent(APIModel):
    display_name: str = Field(alias="displayName")


class ToolInput(APIModel):
    value: int


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


def test_sync_generate_text_uses_typed_chat_models(
    respx_mock: respx.Router,
) -> None:
    route = respx_mock.post(f"{API_URL}/ai/chat/completions").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "chat_1",
                "object": "chat.completion",
                "created": 1,
                "model": "frontal-ai-fast",
                "choices": [
                    {
                        "index": 0,
                        "message": {"role": "assistant", "content": "hello"},
                        "finishReason": "stop",
                    }
                ],
                "usage": {
                    "promptTokens": 2,
                    "completionTokens": 1,
                    "totalTokens": 3,
                },
            },
        )
    )
    client = Frontal("frt_local_key", max_retries=0)

    result = client.ai.generate_text(
        {"model": "frontal-ai-fast", "prompt": "say hello", "maxTokens": 24}
    )

    request_body = json.loads(route.calls.last.request.content)
    assert isinstance(result, GenerateTextResult)
    assert result.text == "hello"
    assert result.usage.total_tokens == 3
    assert request_body["messages"] == [{"role": "user", "content": "say hello"}]
    assert request_body["maxTokens"] == 24
    assert "topP" not in request_body
    client.close()


def test_sync_embed_normalizes_typed_embeddings_response(
    respx_mock: respx.Router,
) -> None:
    route = respx_mock.post(f"{API_URL}/internal/embeddings").mock(
        return_value=httpx.Response(
            200,
            json={
                "object": "list",
                "data": [{"object": "embedding", "embedding": [0.1, 0.2], "index": 0}],
                "model": "embed-model",
                "usage": {"promptTokens": 2, "totalTokens": 2},
            },
        )
    )
    client = Frontal("frt_local_key", max_retries=0)

    result = client.ai.embed("embed-model", "hello")

    assert result.embeddings == [[0.1, 0.2]]
    assert result.usage.total_tokens == 2
    assert json.loads(route.calls.last.request.content) == {
        "model": "embed-model",
        "input": "hello",
    }
    client.close()


def test_sync_generate_object_and_image_helpers(respx_mock: respx.Router) -> None:
    respx_mock.post(f"{API_URL}/ai/chat/completions").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "chat_json",
                "object": "chat.completion",
                "created": 1,
                "model": "frontal-ai-fast",
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": '{"displayName":"Ada"}',
                        },
                        "finishReason": "stop",
                    }
                ],
                "usage": {
                    "promptTokens": 3,
                    "completionTokens": 2,
                    "totalTokens": 5,
                },
            },
        )
    )
    image_route = respx_mock.post(f"{API_URL}/internal/predictions").mock(
        return_value=httpx.Response(
            200, json={"data": [{"url": "https://images.test/ada.png"}]}
        )
    )
    client = Frontal("frt_local_key", max_retries=0)

    generated = client.ai.generate_object(
        model="frontal-ai-fast", prompt="Return Ada", schema=CreateAgent
    )
    image = client.ai.generate_image({"prompt": "A friendly Ada portrait"})

    assert isinstance(generated, GenerateObjectResult)
    assert generated.object == CreateAgent(display_name="Ada")
    assert generated.usage.total_tokens == 5
    assert isinstance(image, GenerateImageResult)
    assert image.images[0].url == "https://images.test/ada.png"
    assert json.loads(image_route.calls.last.request.content) == {
        "prompt": "A friendly Ada portrait",
        "model": "dall-e-3",
        "n": 1,
        "size": "1024x1024",
        "responseFormat": "url",
    }
    client.close()


async def test_async_moderation_rerank_and_speech_helpers(
    respx_mock: respx.Router,
) -> None:
    def prediction_response(request: httpx.Request) -> httpx.Response:
        request_body = json.loads(request.content)
        if "voice" in request_body:
            return httpx.Response(
                200,
                content=b"audio",
                headers={"content-type": "audio/mpeg"},
            )
        return httpx.Response(
            200,
            json={
                "id": "moderation_1",
                "model": "text-moderation-latest",
                "results": [
                    {
                        "flagged": False,
                        "categories": {"violence": False},
                        "categoryScores": {"violence": 0.01},
                    }
                ],
            },
        )

    prediction_route = respx_mock.post(f"{API_URL}/internal/predictions").mock(
        side_effect=prediction_response
    )
    rerank_route = respx_mock.post(f"{API_URL}/internal/rerank").mock(
        return_value=httpx.Response(200, json={"scores": [0.9, 0.2]})
    )
    client = AsyncFrontal("frt_local_key", max_retries=0)

    moderation = await client.ai.moderate({"input": "hello"})
    rerank = await client.ai.rerank(
        {
            "model": "rerank-v1",
            "query": "SDK",
            "documents": ["Python SDK", {"content": "Other", "chunkIndex": 2}],
        }
    )
    speech = await client.ai.generate_speech(
        {"text": "hello", "voice": "alloy", "format": "mp3"}
    )

    assert moderation.results[0].flagged is False
    assert rerank.scores == [0.9, 0.2]
    assert speech == b"audio"
    rerank_body = json.loads(rerank_route.calls.last.request.content)
    assert rerank_body["documents"] == [
        {"content": "Python SDK"},
        {"content": "Other", "chunkIndex": 2},
    ]
    assert prediction_route.call_count == 2
    assert json.loads(prediction_route.calls.last.request.content) == {
        "model": "tts-1",
        "input": "hello",
        "voice": "alloy",
        "responseFormat": "mp3",
    }
    await client.aclose()


def test_sync_generate_text_executes_tool_loop(respx_mock: respx.Router) -> None:
    route = respx_mock.post(f"{API_URL}/ai/chat/completions").mock(
        side_effect=[
            httpx.Response(
                200,
                json={
                    "id": "chat_tool_1",
                    "object": "chat.completion",
                    "created": 1,
                    "model": "frontal-ai-fast",
                    "choices": [
                        {
                            "index": 0,
                            "message": {
                                "role": "assistant",
                                "toolCalls": [
                                    {
                                        "id": "call_1",
                                        "type": "function",
                                        "function": {
                                            "name": "double",
                                            "arguments": '{"value":4}',
                                        },
                                    }
                                ],
                            },
                            "finishReason": "tool_calls",
                        }
                    ],
                    "usage": {
                        "promptTokens": 2,
                        "completionTokens": 1,
                        "totalTokens": 3,
                    },
                },
            ),
            httpx.Response(
                200,
                json={
                    "id": "chat_tool_2",
                    "object": "chat.completion",
                    "created": 1,
                    "model": "frontal-ai-fast",
                    "choices": [
                        {
                            "index": 0,
                            "message": {"role": "assistant", "content": "8"},
                            "finishReason": "stop",
                        }
                    ],
                    "usage": {
                        "promptTokens": 5,
                        "completionTokens": 1,
                        "totalTokens": 6,
                    },
                },
            ),
        ]
    )
    client = Frontal("frt_local_key", max_retries=0)

    result = client.ai.generate_text(
        {
            "model": "frontal-ai-fast",
            "prompt": "Double four",
            "maxSteps": 2,
            "tools": {
                "double": tool(
                    description="Double a number",
                    parameters=ToolInput,
                    execute=lambda value: {"value": value.value * 2},
                )
            },
        }
    )

    assert result.text == "8"
    assert len(result.steps) == 2
    assert result.usage.total_tokens == 9
    assert result.steps[0].tool_results[0].output == {"value": 8}
    first_request = json.loads(route.calls[0].request.content)
    second_request = json.loads(route.calls[1].request.content)
    assert first_request["tools"][0]["function"]["name"] == "double"
    assert second_request["messages"][-1]["role"] == "tool"
    assert second_request["messages"][-1]["content"] == '{"value": 8}'
    client.close()


def test_sync_stream_text_yields_text_finish_and_done(
    respx_mock: respx.Router,
) -> None:
    route = respx_mock.post(f"{API_URL}/ai/chat/completions").mock(
        return_value=httpx.Response(
            200,
            headers={"content-type": "text/event-stream"},
            content=_sse_response(
                [
                    {"choices": [{"delta": {"content": "hello "}}]},
                    {
                        "choices": [
                            {"delta": {"content": "world"}, "finishReason": "stop"}
                        ],
                        "usage": {
                            "promptTokens": 2,
                            "completionTokens": 2,
                            "totalTokens": 4,
                        },
                    },
                    "[DONE]",
                ]
            ),
        )
    )
    client = Frontal("frt_local_key", max_retries=0)
    chunks: list[str] = []

    parts = list(
        client.ai.stream_text(
            {
                "model": "frontal-ai-fast",
                "prompt": "Say hello",
                "onChunk": chunks.append,
            }
        )
    )

    assert [part.type for part in parts] == ["text", "text", "finish", "done"]
    assert [part.text for part in parts[:2]] == ["hello ", "world"]
    assert parts[2].usage.total_tokens == 4
    assert chunks == ["hello ", "world"]
    assert json.loads(route.calls.last.request.content)["stream"] is True
    client.close()


def test_stream_text_retries_retryable_response_before_first_event(
    respx_mock: respx.Router, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("frontal_sdk.core.http.time_sleep", lambda _delay: None)
    route = respx_mock.post(f"{API_URL}/ai/chat/completions").mock(
        side_effect=[
            httpx.Response(503, json={"message": "try again"}),
            httpx.Response(
                200,
                headers={"content-type": "text/event-stream"},
                content=_sse_response(
                    [
                        {"choices": [{"delta": {"content": "ok"}}]},
                        "[DONE]",
                    ]
                ),
            ),
        ]
    )
    client = Frontal("frt_local_key", max_retries=0)

    parts = list(
        client.ai.stream_text(
            {
                "model": "frontal-ai-fast",
                "prompt": "retry",
                "streamRetries": 1,
            }
        )
    )

    assert route.call_count == 2
    assert [part.type for part in parts] == ["text", "finish", "done"]
    client.close()


async def test_async_stream_text_assembles_tool_call_deltas(
    respx_mock: respx.Router,
) -> None:
    respx_mock.post(f"{API_URL}/ai/chat/completions").mock(
        return_value=httpx.Response(
            200,
            headers={"content-type": "text/event-stream"},
            content=_sse_response(
                [
                    {
                        "choices": [
                            {
                                "delta": {
                                    "toolCalls": [
                                        {
                                            "index": 0,
                                            "id": "call_1",
                                            "function": {
                                                "name": "lookup",
                                                "arguments": '{"id":',
                                            },
                                        }
                                    ]
                                }
                            }
                        ]
                    },
                    {
                        "choices": [
                            {
                                "delta": {
                                    "toolCalls": [
                                        {
                                            "index": 0,
                                            "function": {"arguments": "1}"},
                                        }
                                    ]
                                },
                                "finishReason": "tool_calls",
                            }
                        ],
                        "usage": {
                            "promptTokens": 1,
                            "completionTokens": 1,
                            "totalTokens": 2,
                        },
                    },
                    "[DONE]",
                ]
            ),
        )
    )
    client = AsyncFrontal("frt_local_key", max_retries=0)

    parts = [
        part async for part in client.ai.stream_text({"model": "m", "prompt": "go"})
    ]

    assert [part.type for part in parts] == ["tool-call", "finish", "done"]
    assert parts[0].tool_name == "lookup"
    assert parts[0].input == {"id": 1}
    assert parts[1].finish_reason == "tool-calls"
    await client.aclose()


async def test_async_generate_text_runs_async_tool_executor(
    respx_mock: respx.Router,
) -> None:
    respx_mock.post(f"{API_URL}/ai/chat/completions").mock(
        side_effect=[
            httpx.Response(
                200,
                json={
                    "id": "chat_async_tool_1",
                    "object": "chat.completion",
                    "created": 1,
                    "model": "frontal-ai-fast",
                    "choices": [
                        {
                            "index": 0,
                            "message": {
                                "role": "assistant",
                                "toolCalls": [
                                    {
                                        "id": "call_2",
                                        "type": "function",
                                        "function": {
                                            "name": "double",
                                            "arguments": '{"value":3}',
                                        },
                                    }
                                ],
                            },
                            "finishReason": "tool_calls",
                        }
                    ],
                    "usage": {
                        "promptTokens": 1,
                        "completionTokens": 1,
                        "totalTokens": 2,
                    },
                },
            ),
            httpx.Response(
                200,
                json={
                    "id": "chat_async_tool_2",
                    "object": "chat.completion",
                    "created": 1,
                    "model": "frontal-ai-fast",
                    "choices": [
                        {
                            "index": 0,
                            "message": {"role": "assistant", "content": "6"},
                            "finishReason": "stop",
                        }
                    ],
                    "usage": {
                        "promptTokens": 3,
                        "completionTokens": 1,
                        "totalTokens": 4,
                    },
                },
            ),
        ]
    )
    client = AsyncFrontal("frt_local_key", max_retries=0)

    async def double(value: Any) -> dict[str, int]:
        return {"value": value.value * 2}

    result = await client.ai.generate_text(
        {
            "model": "frontal-ai-fast",
            "prompt": "Double three",
            "maxSteps": 2,
            "tools": {
                "double": tool(
                    description="Double a number",
                    parameters=ToolInput,
                    execute=double,
                )
            },
        }
    )

    assert result.text == "6"
    assert result.usage.total_tokens == 6
    assert result.steps[0].tool_results[0].output == {"value": 6}
    await client.aclose()


def test_agent_builder_validates_and_sends_defaults(
    respx_mock: respx.Router,
) -> None:
    route = respx_mock.post(f"{API_URL}/agents").mock(
        return_value=httpx.Response(201, json={"id": "agent_1"})
    )
    client = Frontal("frt_local_key", max_retries=0)

    result = (
        client.agents.define("ticket-triager")
        .description("Triage support tickets")
        .trigger("support.ticket.created")
        .can_read("ticket")
        .tags("support")
        .create()
    )

    request_body = json.loads(route.calls.last.request.content)
    assert result == {"id": "agent_1"}
    assert request_body["triggers"] == [{"event": "support.ticket.created"}]
    assert request_body["scope"]["read"] == ["ticket"]
    assert request_body["confidence"]["autoExecuteAbove"] == 0.85
    assert request_body["retry"]["backoff"] == "exponential"
    assert "rateLimit" not in request_body
    client.close()


def test_agent_configure_json_and_approval_predicate(
    respx_mock: respx.Router,
) -> None:
    respx_mock.post(f"{API_URL}/agents").mock(
        return_value=httpx.Response(201, json={"id": "agent_approval"})
    )
    client = Frontal("frt_local_key", max_retries=0)
    builder = client.agents.define(
        "approval-agent",
        {"description": "Classify tickets", "triggers": "ticket.created"},
    )

    definition = builder.to_json()
    accessor = client.agents.use(
        "agent_approval", approve_when=lambda state: state.get("risk") == "high"
    )

    assert definition["description"] == "Classify tickets"
    assert definition["triggers"] == [{"event": "ticket.created"}]
    assert accessor.requires_approval({"risk": "high"})
    assert not accessor.requires_approval({"risk": "low"})
    client.close()


def test_sync_ai_legacy_tool_registry_validates_input() -> None:
    client = Frontal("frt_local_key", max_retries=0)
    registered = client.ai.define_tool(
        "double",
        description="Double an integer",
        parameters=ToolInput,
        execute=lambda value: value.value * 2,
    )
    client.ai.register_tool(registered)

    assert client.ai.get_tools() == [registered]
    assert client.ai.execute_tool("double", {"value": "4"}) == 8
    with pytest.raises(ValueError, match="Tool not found"):
        client.ai.execute_tool("missing", {})
    client.close()


@pytest.mark.anyio
async def test_async_ai_legacy_tool_registry_awaits_result() -> None:
    async with AsyncFrontal("frt_local_key", max_retries=0) as client:

        async def double(value: ToolInput) -> int:
            return value.value * 2

        registered = client.ai.define_tool(
            "double",
            description="Double an integer",
            parameters=ToolInput,
            execute=double,
        )
        client.ai.register_tool(registered)

        assert await client.ai.execute_tool("double", {"value": 5}) == 10


def test_sync_agent_wait_for_completion_polls_until_terminal(
    respx_mock: respx.Router,
) -> None:
    route = respx_mock.get(f"{API_URL}/agents/runs/run_1").mock(
        side_effect=[
            httpx.Response(200, json={"status": "running"}),
            httpx.Response(200, json={"status": "completed"}),
        ]
    )
    client = Frontal("frt_local_key", max_retries=0)

    result = client.agents.use("agent_1").wait_for_completion(
        "run_1", interval=0.001, timeout=1
    )

    assert result == {"status": "completed"}
    assert route.call_count == 2
    client.close()


@pytest.mark.anyio
async def test_async_agent_wait_for_completion_polls_without_sync_transport(
    respx_mock: respx.Router,
) -> None:
    route = respx_mock.get(f"{API_URL}/agents/runs/run_2").mock(
        side_effect=[
            httpx.Response(200, json={"status": "running"}),
            httpx.Response(200, json={"status": "failed"}),
        ]
    )
    async with AsyncFrontal("frt_local_key", max_retries=0) as client:
        result = await client.agents.use("agent_1").wait_for_completion(
            "run_2", interval=0.001, timeout=1
        )

    assert result == {"status": "failed"}
    assert route.call_count == 2


def test_workflow_builder_creates_base_and_version(
    respx_mock: respx.Router,
) -> None:
    create_route = respx_mock.post(f"{API_URL}/workflows").mock(
        return_value=httpx.Response(
            201,
            json={
                "workflow": {
                    "id": "workflow_1",
                    "name": "Café handoff",
                    "status": "draft",
                }
            },
        )
    )
    version_route = respx_mock.post(f"{API_URL}/workflows/workflow_1/versions").mock(
        return_value=httpx.Response(201, json={"latestVersion": 1})
    )
    client = Frontal("frt_local_key", max_retries=0)

    result = (
        client.workflows.define("Café handoff")
        .description("Review incoming requests")
        .version("1.0.0")
        .manual()
        .task("review", {"queue": "support"}, timeout="30s")
        .approval("approve", ["manager"], depends_on=["review"])
        .tags("support")
        .create()
    )

    base_body = json.loads(create_route.calls.last.request.content)
    version_body = json.loads(version_route.calls.last.request.content)
    assert base_body == {
        "name": "Café handoff",
        "slug": "cafe-handoff",
        "description": "Review incoming requests",
    }
    assert version_body["spec"]["triggers"] == [{"type": "manual"}]
    assert version_body["spec"]["steps"][1]["dependsOn"] == ["review"]
    assert result["id"] == "workflow_1"
    assert result["version"] == 1
    client.close()


async def test_async_workflow_builder_creates_base_and_version(
    respx_mock: respx.Router,
) -> None:
    create_route = respx_mock.post(f"{API_URL}/workflows").mock(
        return_value=httpx.Response(
            201,
            json={"workflow": {"workflowId": "workflow_2", "status": "draft"}},
        )
    )
    version_route = respx_mock.post(f"{API_URL}/workflows/workflow_2/versions").mock(
        return_value=httpx.Response(201, json={"latestVersion": 2})
    )
    client = AsyncFrontal("frt_local_key", max_retries=0)

    result = await (
        client.workflows.define("Async workflow")
        .event("ticket.created", {"priority": "high"})
        .delay("wait", "5m")
        .create()
    )

    assert (
        json.loads(create_route.calls.last.request.content)["slug"] == "async-workflow"
    )
    assert (
        json.loads(version_route.calls.last.request.content)["spec"]["steps"][0]["type"]
        == "delay"
    )
    assert result["id"] == "workflow_2"
    assert result["version"] == 2
    await client.aclose()


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


def test_sync_sse_stream_does_not_retry_after_yielding_an_event(
    respx_mock: respx.Router,
) -> None:
    route = respx_mock.get(f"{API_URL}/agents/runs/run_1/stream").mock(
        return_value=httpx.Response(
            200,
            headers={"Content-Type": "text/event-stream"},
            stream=_InterruptedSyncSSE(),
        )
    )
    client = Frontal("frt_local_key", max_retries=2)
    events = client.agents.stream_agents_runs_by_param_1_stream("run_1")

    assert next(events) == ServerEvent("message", {"step": 1}, None)
    with pytest.raises(NetworkError, match="Stream request failed"):
        next(events)

    assert route.call_count == 1
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
async def test_async_generate_text_uses_typed_chat_models(
    respx_mock: respx.Router,
) -> None:
    respx_mock.post(f"{API_URL}/ai/chat/completions").mock(
        return_value=httpx.Response(
            200,
            json={
                "id": "chat_1",
                "object": "chat.completion",
                "created": 1,
                "model": "frontal-ai-fast",
                "choices": [
                    {
                        "index": 0,
                        "message": {"role": "assistant", "content": "async hello"},
                        "finishReason": "stop",
                    }
                ],
            },
        )
    )
    async with AsyncFrontal("frt_local_key", max_retries=0) as client:
        result = await client.ai.generate_text(
            {"model": "frontal-ai-fast", "prompt": "say hello"}
        )

    assert isinstance(result, GenerateTextResult)
    assert result.text == "async hello"
    assert result.usage.total_tokens == 0


@pytest.mark.anyio
async def test_async_agent_builder_uses_async_transport(
    respx_mock: respx.Router,
) -> None:
    route = respx_mock.post(f"{API_URL}/agents").mock(
        return_value=httpx.Response(201, json={"id": "agent_1"})
    )
    async with AsyncFrontal("frt_local_key", max_retries=0) as client:
        result = await (
            client.agents.define("ticket-triager")
            .trigger("support.ticket.created")
            .create()
        )

    assert result == {"id": "agent_1"}
    assert json.loads(route.calls.last.request.content)["triggers"] == [
        {"event": "support.ticket.created"}
    ]


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


@pytest.mark.anyio
async def test_async_sse_stream_does_not_retry_after_yielding_an_event(
    respx_mock: respx.Router,
) -> None:
    route = respx_mock.get(f"{API_URL}/agents/runs/run_2/stream").mock(
        return_value=httpx.Response(
            200,
            headers={"Content-Type": "text/event-stream"},
            stream=_InterruptedAsyncSSE(),
        )
    )
    async with AsyncFrontal("frt_local_key", max_retries=2) as client:
        events = client.agents.stream_agents_runs_by_param_1_stream("run_2")
        assert await events.__anext__() == ServerEvent("message", {"step": 1}, None)
        with pytest.raises(NetworkError, match="Stream request failed"):
            await events.__anext__()

    assert route.call_count == 1


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

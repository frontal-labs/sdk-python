"""Run standalone examples without a live API."""

from __future__ import annotations

import runpy

import httpx
import pytest
import respx

API_URL = "https://api.frontal.dev/v1"


def _set_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FRONTAL_API_KEY", "frt_example_test_key")


def _chat_response() -> httpx.Response:
    return httpx.Response(
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


def test_quickstart_example_with_mocked_chat_completion(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _set_api_key(monkeypatch)
    with respx.mock(assert_all_called=False) as router:
        route = router.post(f"{API_URL}/ai/chat/completions").mock(
            side_effect=lambda _request: _chat_response()
        )
        runpy.run_path("examples/quickstart.py", run_name="__main__")
    assert route.called


def test_async_quickstart_example_with_mocked_chat_completion(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _set_api_key(monkeypatch)
    with respx.mock(assert_all_called=False) as router:
        route = router.post(f"{API_URL}/ai/chat/completions").mock(
            side_effect=lambda _request: _chat_response()
        )
        runpy.run_path("examples/async_quickstart.py", run_name="__main__")
    assert route.called


def test_agent_definition_example_with_mocked_api(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _set_api_key(monkeypatch)
    with respx.mock(assert_all_called=False) as router:
        route = router.post(f"{API_URL}/agents").mock(
            return_value=httpx.Response(201, json={"id": "agent_1"})
        )
        runpy.run_path("examples/define_agent.py", run_name="__main__")
    assert route.called


def test_workflow_example_with_mocked_api(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _set_api_key(monkeypatch)
    with respx.mock(assert_all_called=False) as router:
        create_route = router.post(f"{API_URL}/workflows").mock(
            return_value=httpx.Response(
                201,
                json={
                    "workflow": {
                        "id": "workflow_1",
                        "name": "Support ticket handoff",
                        "status": "draft",
                    }
                },
            )
        )
        version_route = router.post(f"{API_URL}/workflows/workflow_1/versions").mock(
            return_value=httpx.Response(201, json={"latestVersion": 1})
        )
        trigger_route = router.post(f"{API_URL}/workflows/executions").mock(
            return_value=httpx.Response(
                201, json={"execution": {"id": "execution_1", "status": "pending"}}
            )
        )
        runpy.run_path("examples/create_workflow.py", run_name="__main__")
    assert create_route.called
    assert version_route.called
    assert trigger_route.called

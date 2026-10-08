"""Run the standalone quickstart without a live API."""

from __future__ import annotations

import runpy

import httpx
import pytest
import respx


def test_quickstart_example_with_mocked_chat_completion(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("FRONTAL_API_KEY", "frt_example_test_key")
    with respx.mock(assert_all_called=False) as router:
        route = router.post("https://api.frontal.dev/v1/ai/chat/completions").mock(
            side_effect=lambda _request: httpx.Response(
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
        runpy.run_path("examples/quickstart.py", run_name="__main__")
    assert route.called

"""Execute Python examples embedded in the README against mocked HTTP."""

from __future__ import annotations

from pathlib import Path
from re import DOTALL, findall

import httpx
import pytest
import respx

API_URL = "https://api.frontal.dev/v1"


def test_readme_python_fences_run_against_mocked_http(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("FRONTAL_API_KEY", "frt_docs_test_key")
    source = Path("README.md").read_text(encoding="utf-8")
    code_blocks = findall(r"```python\s*\n(.*?)\n```", source, flags=DOTALL)
    assert code_blocks, "README should keep at least one executable Python example"

    with respx.mock(assert_all_called=False) as router:
        router.post(f"{API_URL}/ai/chat/completions").mock(
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
        for number, code in enumerate(code_blocks, start=1):
            exec(compile(code, f"README.md:python-fence-{number}", "exec"), {})

"""Run the standalone quickstart without a live API."""

from __future__ import annotations

import runpy

import httpx
import pytest
import respx


def test_quickstart_example_with_mocked_health(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("FRONTAL_API_KEY", "frt_example_test_key")
    with respx.mock(assert_all_called=False) as router:
        route = router.get("https://api.frontal.dev/v1/health").mock(
            side_effect=lambda _request: httpx.Response(200, json={"status": "ok"})
        )
        runpy.run_path("examples/quickstart.py", run_name="__main__")
    assert route.called

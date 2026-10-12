"""Circuit breaker tests covering state transitions and lock safety."""

from __future__ import annotations

import asyncio
import threading
import time
from typing import Any, Callable

import pytest
from frontal_sdk import core
from frontal_sdk.core.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitBreakerOpenError,
    CircuitState,
)


def _boom() -> Any:
    raise RuntimeError("upstream is down")


def _ok() -> str:
    return "ok"


def _server_error() -> int:
    return 500


def _fail_once(breaker: CircuitBreaker) -> None:
    """Drive one failure through the breaker on the calling thread."""
    with pytest.raises(RuntimeError):
        breaker.execute(_boom)


def _succeed_once(breaker: CircuitBreaker) -> str:
    return breaker.execute(_ok)


def _run_with_timeout(fn: Callable[[], Any], timeout: float = 5.0) -> Any:
    """Run ``fn`` on a worker thread, failing instead of hanging on deadlock."""
    outcome: list[Any] = []
    failure: list[BaseException] = []

    def runner() -> None:
        try:
            outcome.append(fn())
        except BaseException as exc:  # noqa: BLE001 - re-raised below by the caller
            failure.append(exc)

    thread = threading.Thread(target=runner, daemon=True)
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        pytest.fail("circuit breaker deadlocked")
    if failure:
        raise failure[0]
    return outcome[0]


def test_public_core_exports_expose_breaker_names() -> None:
    assert core.CircuitBreaker is CircuitBreaker
    assert core.CircuitBreakerOpenError is CircuitBreakerOpenError
    assert "CircuitBreakerOpenError" in core.__all__
    assert "CircuitState" in core.__all__


def test_open_callback_may_read_breaker_state() -> None:
    observed: list[tuple[CircuitState, int]] = []

    def on_open() -> None:
        # Deadlocks if the callback fires while the breaker lock is held.
        observed.append((breaker.state, breaker.failures))

    breaker = CircuitBreaker(CircuitBreakerConfig(failure_threshold=1, on_open=on_open))

    with pytest.raises(RuntimeError):
        _run_with_timeout(lambda: breaker.execute(_boom))

    assert observed == [("open", 1)]


def test_close_callback_may_read_breaker_state() -> None:
    observed: list[tuple[CircuitState, int]] = []

    def on_close() -> None:
        # Deadlocks if the callback fires while the breaker lock is held.
        observed.append((breaker.state, breaker.failures))

    breaker = CircuitBreaker(
        CircuitBreakerConfig(failure_threshold=1, reset_timeout=0.01, on_close=on_close)
    )

    _run_with_timeout(lambda: _fail_once(breaker))
    time.sleep(0.02)
    assert _run_with_timeout(lambda: _succeed_once(breaker)) == "ok"

    assert observed == [("closed", 0)]


def test_half_open_callback_may_read_breaker_state() -> None:
    observed: list[CircuitState] = []

    def on_half_open() -> None:
        observed.append(breaker.state)

    breaker = CircuitBreaker(
        CircuitBreakerConfig(
            failure_threshold=1, reset_timeout=0.01, on_half_open=on_half_open
        )
    )

    _run_with_timeout(lambda: _fail_once(breaker))
    time.sleep(0.02)
    assert _run_with_timeout(lambda: _succeed_once(breaker)) == "ok"

    assert observed == ["half_open"]


@pytest.mark.parametrize(
    "cancelled",
    [asyncio.CancelledError, KeyboardInterrupt, SystemExit],
)
def test_non_error_base_exceptions_do_not_open_the_circuit(
    cancelled: type[BaseException],
) -> None:
    def _cancelled() -> Any:
        raise cancelled("stopped")

    breaker = CircuitBreaker(CircuitBreakerConfig(failure_threshold=1))

    with pytest.raises(cancelled):
        breaker.execute(_cancelled)

    assert breaker.state == "closed"
    assert breaker.failures == 0


def test_failures_open_the_circuit_and_short_circuit_calls() -> None:
    breaker = CircuitBreaker(CircuitBreakerConfig(failure_threshold=2))

    for _ in range(2):
        with pytest.raises(RuntimeError):
            breaker.execute(_boom)

    assert breaker.state == "open"
    assert breaker.failures == 2
    with pytest.raises(CircuitBreakerOpenError):
        breaker.execute(_ok)


def test_successful_probe_closes_the_circuit() -> None:
    breaker = CircuitBreaker(
        CircuitBreakerConfig(failure_threshold=1, reset_timeout=0.01)
    )

    with pytest.raises(RuntimeError):
        breaker.execute(_boom)
    assert breaker.state == "open"

    time.sleep(0.02)
    assert breaker.execute(_ok) == "ok"
    assert breaker.state == "closed"
    assert breaker.failures == 0


def test_result_predicate_counts_non_raising_failures() -> None:
    breaker = CircuitBreaker(CircuitBreakerConfig(failure_threshold=1))

    def is_failure(status: int) -> bool:
        return status >= 500

    assert breaker.execute(_server_error, is_failure=is_failure) == 500

    assert breaker.state == "open"
    with pytest.raises(CircuitBreakerOpenError):
        breaker.execute(_ok)


def test_force_close_reopens_and_accepts_a_new_probe() -> None:
    breaker = CircuitBreaker(
        CircuitBreakerConfig(failure_threshold=1, reset_timeout=10)
    )
    _fail_once(breaker)
    _run_with_timeout(breaker.force_close)
    assert breaker.state == "closed"
    assert breaker.failures == 0
    assert _run_with_timeout(lambda: _succeed_once(breaker)) == "ok"


async def test_async_cancel_does_not_open_the_circuit() -> None:
    async def _cancelled() -> Any:
        raise asyncio.CancelledError("stopped")

    breaker = CircuitBreaker(CircuitBreakerConfig(failure_threshold=1))

    with pytest.raises(asyncio.CancelledError):
        await breaker.execute_async(_cancelled)

    assert breaker.state == "closed"
    assert breaker.failures == 0


async def test_async_failures_open_the_circuit() -> None:
    async def _boom_async() -> Any:
        raise RuntimeError("upstream is down")

    async def _ok_async() -> str:
        return "ok"

    breaker = CircuitBreaker(CircuitBreakerConfig(failure_threshold=1))
    with pytest.raises(RuntimeError):
        await breaker.execute_async(_boom_async)

    assert breaker.state == "open"
    with pytest.raises(CircuitBreakerOpenError):
        await breaker.execute_async(_ok_async)

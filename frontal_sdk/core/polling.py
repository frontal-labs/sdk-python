"""Polling helpers for long-running API operations."""

from __future__ import annotations

import time
from collections.abc import Awaitable, Callable
from math import isfinite
from typing import Literal, TypeVar

import anyio

from frontal_sdk.core.errors import TimeoutError

ResultT = TypeVar("ResultT")
Backoff = Literal["constant", "linear", "exponential"]


def poll_until(
    fetch: Callable[[], ResultT],
    *,
    until: Callable[[ResultT], bool] | None = None,
    interval: float = 2.0,
    timeout: float = 300.0,
    backoff: Backoff = "constant",
) -> ResultT:
    """Call ``fetch`` until its result satisfies ``until`` or times out."""
    _validate_polling(interval, timeout, backoff)
    predicate = until or bool
    started = time.monotonic()
    attempt = 0
    while True:
        result = fetch()
        if predicate(result):
            return result
        remaining = timeout - (time.monotonic() - started)
        if remaining <= 0:
            raise TimeoutError(f"Polling timed out after {timeout:g} seconds")
        time.sleep(min(_poll_delay(interval, attempt, backoff), remaining))
        attempt += 1


async def async_poll_until(
    fetch: Callable[[], Awaitable[ResultT]],
    *,
    until: Callable[[ResultT], bool] | None = None,
    interval: float = 2.0,
    timeout: float = 300.0,
    backoff: Backoff = "constant",
) -> ResultT:
    """Asynchronously poll until a result matches or the timeout expires."""
    _validate_polling(interval, timeout, backoff)
    predicate = until or bool
    started = time.monotonic()
    attempt = 0
    while True:
        result = await fetch()
        if predicate(result):
            return result
        remaining = timeout - (time.monotonic() - started)
        if remaining <= 0:
            raise TimeoutError(f"Polling timed out after {timeout:g} seconds")
        await anyio.sleep(min(_poll_delay(interval, attempt, backoff), remaining))
        attempt += 1


def _validate_polling(interval: float, timeout: float, backoff: Backoff) -> None:
    if not isfinite(interval) or interval <= 0:
        raise ValueError("interval must be a finite positive number")
    if not isfinite(timeout) or timeout <= 0:
        raise ValueError("timeout must be a finite positive number")
    if backoff not in {"constant", "linear", "exponential"}:
        raise ValueError("unsupported polling backoff strategy")


def _poll_delay(interval: float, attempt: int, backoff: Backoff) -> float:
    if backoff == "linear":
        return interval * (attempt + 1)
    if backoff == "exponential":
        return interval * float(2**attempt)
    return interval


__all__ = ["async_poll_until", "poll_until"]

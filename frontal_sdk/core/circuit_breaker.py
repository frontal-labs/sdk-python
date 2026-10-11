"""Circuit breaker that guards API calls from cascading failures."""

from __future__ import annotations

import threading
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Literal, TypeVar

from frontal_sdk.core.errors import FrontalError

CircuitState = Literal["closed", "open", "half_open"]

ResultT = TypeVar("ResultT")


@dataclass(frozen=True)
class CircuitBreakerConfig:
    """Configuration for :class:`CircuitBreaker`.

    ``failure_threshold`` consecutive failures open the circuit;
    ``reset_timeout`` seconds later it half-opens and lets one
    probe request through. The ``on_*`` callbacks fire on the
    matching transition.
    """

    failure_threshold: int = 5
    reset_timeout: float = 30.0
    on_open: Callable[[], None] | None = None
    on_close: Callable[[], None] | None = None
    on_half_open: Callable[[], None] | None = None

    def __post_init__(self) -> None:
        if (
            isinstance(self.failure_threshold, bool)
            or not isinstance(self.failure_threshold, int)
        ):
            raise TypeError("failure_threshold must be an integer")
        if self.failure_threshold < 1:
            raise ValueError("failure_threshold must be positive")
        if not isinstance(self.reset_timeout, (int, float)):
            raise TypeError("reset_timeout must be a number")
        if self.reset_timeout <= 0:
            raise ValueError("reset_timeout must be positive")


class CircuitBreakerOpenError(FrontalError):
    """A request was rejected because the circuit breaker is open."""

    def __init__(self, retry_after: float) -> None:
        super().__init__(
            f"Circuit breaker is open — retry after {retry_after:g} seconds",
            code="CIRCUIT_BREAKER_OPEN",
        )
        self.retry_after = retry_after


class CircuitBreaker:
    """Counts consecutive failures and short-circuits requests.

    While the circuit is ``open`` (or a half-open probe is in
    flight) calls raise :class:`CircuitBreakerOpenError` instead of
    reaching the API. A successful probe closes the circuit again.
    """

    def __init__(self, config: CircuitBreakerConfig | None = None) -> None:
        self._config = config or CircuitBreakerConfig()
        self._lock = threading.Lock()
        self._failures = 0
        self._last_failure = 0.0
        self._state: CircuitState = "closed"
        self._probe_in_flight = False

    @property
    def state(self) -> CircuitState:
        """The current circuit state."""
        with self._lock:
            return self._state

    @property
    def failures(self) -> int:
        """The current consecutive failure count."""
        with self._lock:
            return self._failures

    def execute(
        self,
        fn: Callable[[], ResultT],
        is_failure: Callable[[ResultT], bool] | None = None,
    ) -> ResultT:
        """Run ``fn`` through the breaker.

        ``is_failure`` classifies a returned (non-raising) result
        as a failure, so HTTP error responses can count too.
        """
        probe = self._enter()
        try:
            try:
                result = fn()
                failed = is_failure is not None and is_failure(result)
            except BaseException:
                with self._lock:
                    self._record_failure(probe)
                raise
            with self._lock:
                if failed:
                    self._record_failure(probe)
                elif probe:
                    self._reset()
                else:
                    self._failures = 0
            return result
        finally:
            with self._lock:
                if probe:
                    self._probe_in_flight = False

    async def execute_async(
        self,
        fn: Callable[[], Awaitable[ResultT]],
        is_failure: Callable[[ResultT], bool] | None = None,
    ) -> ResultT:
        """Run an awaitable ``fn`` through the breaker."""
        probe = self._enter()
        try:
            try:
                result = await fn()
                failed = is_failure is not None and is_failure(result)
            except BaseException:
                with self._lock:
                    self._record_failure(probe)
                raise
            with self._lock:
                if failed:
                    self._record_failure(probe)
                elif probe:
                    self._reset()
                else:
                    self._failures = 0
            return result
        finally:
            with self._lock:
                if probe:
                    self._probe_in_flight = False

    def force_open(self) -> None:
        """Manually force the circuit into the ``open`` state."""
        with self._lock:
            self._state = "open"
            self._last_failure = time.monotonic()
            self._probe_in_flight = False

    def force_close(self) -> None:
        """Manually reset the circuit to the ``closed`` state."""
        with self._lock:
            self._reset()

    def _enter(self) -> bool:
        """Apply state transitions before a call; return whether
        this call is a half-open probe."""
        with self._lock:
            if self._state == "open":
                elapsed = time.monotonic() - self._last_failure
                if elapsed <= self._config.reset_timeout:
                    raise CircuitBreakerOpenError(
                        self._config.reset_timeout - elapsed
                    )
                self._state = "half_open"
                if self._config.on_half_open is not None:
                    self._config.on_half_open()
            probe = self._state == "half_open"
            if probe:
                if self._probe_in_flight:
                    raise CircuitBreakerOpenError(self._config.reset_timeout)
                self._probe_in_flight = True
            return probe

    def _record_failure(self, probe: bool) -> None:
        self._failures += 1
        self._last_failure = time.monotonic()
        if probe or self._failures >= self._config.failure_threshold:
            if self._state != "open":
                self._state = "open"
                if self._config.on_open is not None:
                    self._config.on_open()

    def _reset(self) -> None:
        self._failures = 0
        self._state = "closed"
        if self._config.on_close is not None:
            self._config.on_close()


__all__ = [
    "CircuitBreaker",
    "CircuitBreakerConfig",
    "CircuitBreakerOpenError",
    "CircuitState",
]

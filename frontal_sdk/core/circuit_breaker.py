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
        if isinstance(self.failure_threshold, bool) or not isinstance(
            self.failure_threshold, int
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

    Transition callbacks are invoked without the breaker lock held,
    so a callback may read :attr:`state` or :attr:`failures`. It must
    not call back into the breaker (for example :meth:`force_close`),
    which recurses instead of blocking.
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
        probe, announce = self._enter()
        _notify(announce)
        try:
            try:
                result = fn()
                failed = is_failure is not None and is_failure(result)
            except Exception:
                with self._lock:
                    announce = self._record_failure(probe)
                _notify(announce)
                raise
            with self._lock:
                announce = self._record(failed, probe)
            _notify(announce)
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
        probe, announce = self._enter()
        _notify(announce)
        try:
            try:
                result = await fn()
                failed = is_failure is not None and is_failure(result)
            except Exception:
                with self._lock:
                    announce = self._record_failure(probe)
                _notify(announce)
                raise
            with self._lock:
                announce = self._record(failed, probe)
            _notify(announce)
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
            announce = self._reset()
        _notify(announce)

    def _enter(self) -> tuple[bool, list[Callable[[], None] | None]]:
        """Apply state transitions before a call.

        Return whether this call is a half-open probe, along with the
        transition callbacks to run once the lock has been released.
        """
        with self._lock:
            announce: list[Callable[[], None] | None] = []
            if self._state == "open":
                elapsed = time.monotonic() - self._last_failure
                if elapsed <= self._config.reset_timeout:
                    raise CircuitBreakerOpenError(self._config.reset_timeout - elapsed)
                self._state = "half_open"
                announce.append(self._config.on_half_open)
            if self._state == "half_open":
                if self._probe_in_flight:
                    raise CircuitBreakerOpenError(self._config.reset_timeout)
                self._probe_in_flight = True
                return True, announce
            return False, announce

    def _record(self, failed: bool, probe: bool) -> list[Callable[[], None] | None]:
        """Record a call that returned, returning the transition to announce.

        The caller holds ``self._lock``; taking it here would self-deadlock.
        """
        if failed:
            return self._record_failure(probe)
        if probe:
            return self._reset()
        self._failures = 0
        return []

    def _record_failure(self, probe: bool) -> list[Callable[[], None] | None]:
        """Count a failure; the caller holds ``self._lock``."""
        self._failures += 1
        self._last_failure = time.monotonic()
        if probe or self._failures >= self._config.failure_threshold:
            if self._state != "open":
                self._state = "open"
                return [self._config.on_open]
        return []

    def _reset(self) -> list[Callable[[], None] | None]:
        """Return the circuit to closed; the caller holds ``self._lock``."""
        self._failures = 0
        self._state = "closed"
        return [self._config.on_close]


def _notify(callbacks: list[Callable[[], None] | None]) -> None:
    """Invoke transition callbacks while no breaker lock is held.

    Callbacks run outside the lock so a callback may read ``state`` or
    ``failures``, or call ``force_close``, without deadlocking the breaker.
    """
    for callback in callbacks:
        if callback is not None:
            callback()


__all__ = [
    "CircuitBreaker",
    "CircuitBreakerConfig",
    "CircuitBreakerOpenError",
    "CircuitState",
]

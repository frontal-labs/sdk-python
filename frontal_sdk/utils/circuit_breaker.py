"""Circuit breaker utilities for the Frontal Python SDK."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Callable, TypeVar

from frontal_sdk.core.circuit_breaker import CircuitBreaker, CircuitBreakerConfig

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


__all__ = ["CircuitBreaker", "CircuitBreakerConfig"]
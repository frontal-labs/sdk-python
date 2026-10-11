"""Circuit breaker utilities for the Frontal Python SDK.

This module re-exports the canonical implementation from
:mod:`frontal_sdk.core.circuit_breaker` so that utility consumers
have a single import location.
"""

from __future__ import annotations

from frontal_sdk.core.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitBreakerOpenError,
    CircuitState,
)

__all__ = [
    "CircuitBreaker",
    "CircuitBreakerConfig",
    "CircuitBreakerOpenError",
    "CircuitState",
]

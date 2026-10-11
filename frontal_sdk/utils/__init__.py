"""Utility functions shared across the Frontal Python SDK.

This package is optional and provides helpers that supplement the
core functionality without being tied to any particular API domain.

Available utilities:
- ``retry`` — backoff delay calculation (see :mod:`frontal_sdk.utils.retry`)
- ``circuit_breaker`` — circuit breaker (see :mod:`frontal_sdk.utils.circuit_breaker`)
- ``constants`` — SDK-wide constants (see :mod:`frontal_sdk.utils.constants`)
- ``errors`` — error helpers (see :mod:`frontal_sdk.utils.errors`)
"""
from frontal_sdk.utils.constants import (  # noqa: F401
    API_KEY_PREFIX,
    DEFAULT_BASE_URL,
    SDK_VERSION,
    DEFAULT_RETRY_ON,
    TRANSIENT_STATUS,
    BREAKER_FAILURE_STATUS,
    EXPONENTIAL_BASE,
    JITTER_MAX,
)
from frontal_sdk.utils.errors import error_for_status, FrontalError, RateLimitError  # noqa: F401
from frontal_sdk.utils.retry import calculate_delay, BackoffStrategy  # noqa: F401
from frontal_sdk.utils.circuit_breaker import CircuitBreaker, CircuitBreakerConfig  # noqa: F401

__all__ = [
    "API_KEY_PREFIX",
    "DEFAULT_BASE_URL",
    "SDK_VERSION",
    "DEFAULT_RETRY_ON",
    "TRANSIENT_STATUS",
    "BREAKER_FAILURE_STATUS",
    "EXPONENTIAL_BASE",
    "JITTER_MAX",
    "error_for_status",
    "FrontalError",
    "RateLimitError",
    "calculate_delay",
    "BackoffStrategy",
    "CircuitBreaker",
    "CircuitBreakerConfig",
]
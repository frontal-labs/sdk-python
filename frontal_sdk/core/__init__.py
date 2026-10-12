"""Core configuration, transport, and error types."""

from __future__ import annotations

from frontal_sdk.core.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitBreakerOpenError,
    CircuitState,
)
from frontal_sdk.core.config import ClientConfig
from frontal_sdk.core.constants import DEFAULT_BASE_URL, SDK_VERSION
from frontal_sdk.core.errors import (
    AuthenticationError,
    ConflictError,
    FrontalError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TimeoutError,
    ValidationError,
)
from frontal_sdk.core.http import AsyncHttpClient, HttpClient
from frontal_sdk.core.operation import Operation
from frontal_sdk.core.pagination import async_paginate, paginate
from frontal_sdk.core.polling import async_poll_until, poll_until
from frontal_sdk.core.retry import BackoffStrategy, calculate_delay

__all__ = [
    "AsyncHttpClient",
    "async_paginate",
    "async_poll_until",
    "AuthenticationError",
    "BackoffStrategy",
    "calculate_delay",
    "CircuitBreaker",
    "CircuitBreakerConfig",
    "CircuitBreakerOpenError",
    "CircuitState",
    "ClientConfig",
    "ConflictError",
    "DEFAULT_BASE_URL",
    "FrontalError",
    "HttpClient",
    "NetworkError",
    "NotFoundError",
    "Operation",
    "paginate",
    "poll_until",
    "RateLimitError",
    "SDK_VERSION",
    "ServerError",
    "TimeoutError",
    "ValidationError",
]

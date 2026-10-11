"""Core configuration, transport, and error types."""

from __future__ import annotations

from frontal_sdk.core.config import ClientConfig
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
from frontal_sdk.core.constants import DEFAULT_BASE_URL, SDK_VERSION
from frontal_sdk.core.circuit_breaker import CircuitBreaker, CircuitBreakerConfig
from frontal_sdk.core.operation import Operation
from frontal_sdk.core.pagination import async_paginate, paginate
from frontal_sdk.core.polling import async_poll_until, poll_until
from frontal_sdk.core.retry import calculate_delay, BackoffStrategy

__all__ = [
    "AsyncHttpClient",
    "BackendProtocol",
    "async_paginate",
    "async_poll_until",
    "AuthenticationError",
    "ClientConfig",
    "ConflictError",
    "CircuitBreaker",
    "CircuitBreakerConfig",
    "FrontalError",
    "HttpClient",
    "NetworkError",
    "NotFoundError",
    "Operation",
    "paginate",
    "poll_until",
    "RateLimitError",
    "ServerError",
    "TimeoutError",
    "ValidationError",
    "calculate_delay",
    "SDK_VERSION",
    "BackoffStrategy",
]

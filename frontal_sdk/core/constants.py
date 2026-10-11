"""Shared constants for the Frontal Python SDK."""

from __future__ import annotations

API_KEY_PREFIX = "frt_"
DEFAULT_BASE_URL = "https://api.frontal.dev/v1"
EXPONENTIAL_BASE = 2
JITTER_MAX = 0.1
SDK_VERSION = "1.0.0"

#: Status codes that trigger an automatic GET retry. Rate limits and
#: server errors are replay-safe; client errors and 408/425 only mark
#: an error as transient, never retried automatically.
DEFAULT_RETRY_ON = (429, 500, 502, 503, 504)

#: Statuses that classify an error as transient (retryable by the
#: caller), matching the wider set the API may report.
TRANSIENT_STATUS = frozenset({408, 425, 429, 500, 502, 503, 504})

#: Server failures the circuit breaker counts towards opening.
BREAKER_FAILURE_STATUS = frozenset({500, 502, 503, 504})

__all__ = [
    "API_KEY_PREFIX",
    "BREAKER_FAILURE_STATUS",
    "DEFAULT_BASE_URL",
    "DEFAULT_RETRY_ON",
    "EXPONENTIAL_BASE",
    "JITTER_MAX",
    "SDK_VERSION",
    "TRANSIENT_STATUS",
]

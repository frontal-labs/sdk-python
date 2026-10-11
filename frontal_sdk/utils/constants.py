"""SDK-wide constants for the Frontal Python SDK."""

API_KEY_PREFIX = "frt_"
DEFAULT_BASE_URL = "https://api.frontal.dev/v1"
SDK_VERSION = "1.0.0"

#: Status codes that trigger an automatic GET retry.
DEFAULT_RETRY_ON = (429, 500, 502, 503, 504)

#: Statuses that classify an error as transient (retryable by the caller).
TRANSIENT_STATUS = frozenset({408, 425, 429, 500, 502, 503, 504})

#: Server failures the circuit breaker counts towards opening.
BREAKER_FAILURE_STATUS = frozenset({500, 502, 503, 504})

#: Backoff base multiplier for exponential delay.
EXPONENTIAL_BASE = 2

#: Maximum jitter (seconds) added to retry delays.
JITTER_MAX = 0.1

__all__ = [
    "API_KEY_PREFIX",
    "DEFAULT_BASE_URL",
    "SDK_VERSION",
    "DEFAULT_RETRY_ON",
    "TRANSIENT_STATUS",
    "BREAKER_FAILURE_STATUS",
    "EXPONENTIAL_BASE",
    "JITTER_MAX",
]
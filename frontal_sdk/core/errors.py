"""Typed errors raised by the Frontal API client."""

from __future__ import annotations

from typing import TypedDict

from frontal_sdk.models.types import ErrorField, JSONValue

_RETRYABLE_STATUS = {408, 425, 429, 500, 502, 503, 504}


class _ErrorContext(TypedDict, total=False):
    request_id: str | None
    status_code: int | None
    details: JSONValue
    fields: list[ErrorField] | None
    safe_to_retry: bool


class FrontalError(Exception):
    """Base class for API, protocol, and network failures."""

    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        request_id: str | None = None,
        status_code: int | None = None,
        transient: bool | None = None,
        safe_to_retry: bool = False,
        details: JSONValue = None,
        fields: list[ErrorField] | None = None,
        fix: str | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code or "FRONTAL_ERROR"
        self.request_id = request_id
        self.status_code = status_code
        self.transient = (
            status_code in _RETRYABLE_STATUS if transient is None else transient
        )
        self.safe_to_retry = safe_to_retry
        self.details = details
        self.fields = fields or []
        self.fix = fix


class AuthenticationError(FrontalError):
    """The API key is invalid or lacks permission for the operation."""


class NotFoundError(FrontalError):
    """The requested resource does not exist or is not visible to this key."""


class ConflictError(FrontalError):
    """The request conflicts with the current resource state."""


class RateLimitError(FrontalError):
    """The API rate limit was exceeded."""

    def __init__(
        self,
        message: str,
        *,
        retry_after: float | None = None,
        code: str | None = None,
        request_id: str | None = None,
        status_code: int | None = 429,
        details: JSONValue = None,
        fields: list[ErrorField] | None = None,
        safe_to_retry: bool = False,
        fix: str | None = None,
    ) -> None:
        super().__init__(
            message,
            code=code,
            request_id=request_id,
            status_code=status_code,
            transient=True,
            safe_to_retry=safe_to_retry,
            details=details,
            fields=fields,
            fix=fix,
        )
        self.retry_after = retry_after


class ValidationError(FrontalError):
    """The API rejected a request payload or query parameter."""


class ServerError(FrontalError):
    """The Frontal API returned a 5xx response."""


class NetworkError(FrontalError):
    """The request could not reach the API or the response was interrupted."""

    def __init__(
        self,
        message: str,
        *,
        code: str | None = "NETWORK_ERROR",
        request_id: str | None = None,
        status_code: int | None = None,
        details: JSONValue = None,
        safe_to_retry: bool = False,
    ) -> None:
        super().__init__(
            message,
            code=code,
            request_id=request_id,
            status_code=status_code,
            transient=True,
            safe_to_retry=safe_to_retry,
            details=details,
        )


class TimeoutError(NetworkError):
    """The request exceeded the configured timeout."""


_API_KEY_HINT = "Check FRONTAL_API_KEY — it must be a valid key starting with frt_."
_NOT_FOUND_HINT = "Verify the resource id belongs to this workspace/environment."
_FIELDS_HINT = "Fix the offending properties listed in `fields`."
_BACKOFF_HINT = "Back off and retry after `retryAfter`, or lower concurrency."
_UNAVAILABLE_HINT = "Service is temporarily unavailable; retry with backoff."
_GENERIC_HINT = "Check the API response for details."

_AUTH_CODES = frozenset({"UNAUTHORIZED", "INVALID_API_KEY"})
_NOT_FOUND_CODES = frozenset({"NOT_FOUND"})
_CONFLICT_CODES = frozenset({"VALIDATION_ERROR"})
_INPUT_CODES = frozenset({"BAD_REQUEST", "VALIDATION_ERROR"})
_RATE_LIMIT_CODES = frozenset({"RATE_LIMITED"})
_UNAVAILABLE_CODES = frozenset({"SERVICE_UNAVAILABLE", "INTERNAL_ERROR"})

# HTTP status -> (error subtype, fix hint, error codes the hint applies to).
_STATUS_ERRORS: dict[int, tuple[type[FrontalError], str, frozenset[str]]] = {
    400: (ValidationError, _FIELDS_HINT, _INPUT_CODES),
    401: (AuthenticationError, _API_KEY_HINT, _AUTH_CODES),
    403: (AuthenticationError, _API_KEY_HINT, _AUTH_CODES),
    404: (NotFoundError, _NOT_FOUND_HINT, _NOT_FOUND_CODES),
    409: (ConflictError, _FIELDS_HINT, _CONFLICT_CODES),
    422: (ValidationError, _FIELDS_HINT, _INPUT_CODES),
    429: (RateLimitError, _BACKOFF_HINT, _RATE_LIMIT_CODES),
}


def error_for_status(
    status_code: int,
    message: str,
    *,
    code: str | None = None,
    request_id: str | None = None,
    details: JSONValue = None,
    fields: list[ErrorField] | None = None,
    retry_after: float | None = None,
    safe_to_retry: bool = False,
) -> FrontalError:
    """Create the public error subtype corresponding to an HTTP status.

    The returned error carries the API's error ``code`` when available and a
    human-readable ``fix`` remediation hint. The ``safe_to_retry`` flag
    indicates whether retrying the same request may succeed (rate limits,
    transient 5xx, network). UIs and agents can branch on this without a
    status table.
    """
    arguments: _ErrorContext = {
        "request_id": request_id,
        "status_code": status_code,
        "details": details,
        "fields": fields,
        "safe_to_retry": safe_to_retry,
    }
    error_type, fix = _classify(status_code, code)
    if error_type is RateLimitError:
        return RateLimitError(
            message, code=code, retry_after=retry_after, fix=fix, **arguments
        )
    return error_type(message, code=code, fix=fix, **arguments)


def _classify(
    status_code: int, code: str | None
) -> tuple[type[FrontalError], str | None]:
    """Map an HTTP status and API error code to an error type and fix hint."""
    if status_code in _STATUS_ERRORS:
        error_type, hint, hint_codes = _STATUS_ERRORS[status_code]
        return error_type, hint if code in hint_codes else None
    if status_code >= 500:
        return ServerError, _UNAVAILABLE_HINT if code in _UNAVAILABLE_CODES else None
    # For unmapped status codes return a generic FrontalError carrying the
    # API's error code when known.
    return FrontalError, _GENERIC_HINT if code is None else None


__all__ = [
    "AuthenticationError",
    "ConflictError",
    "FrontalError",
    "NetworkError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "TimeoutError",
    "ValidationError",
    "error_for_status",
]

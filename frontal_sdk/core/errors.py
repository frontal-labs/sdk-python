"""Typed errors raised by the Frontal API client."""

from __future__ import annotations

from typing import TypedDict

from frontal_sdk.models.types import ErrorField, JSONValue

_RETRYABLE_STATUS = {408, 425, 429, 500, 502, 503, 504}


class _ErrorContext(TypedDict, total=False):
    code: str | None
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
        retryable: bool | None = None,
        safe_to_retry: bool = False,
        details: JSONValue = None,
        fields: list[ErrorField] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code or "FRONTAL_ERROR"
        self.request_id = request_id
        self.status_code = status_code
        self.transient = (
            status_code in _RETRYABLE_STATUS if retryable is None else retryable
        )
        # Kept as a compatibility alias: transient failures are not always safe
        # to replay, especially when the failed request was a write.
        self.retryable = self.transient
        self.safe_to_retry = safe_to_retry
        self.details = details
        self.fields = fields or []


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
    ) -> None:
        super().__init__(
            message,
            code=code,
            request_id=request_id,
            status_code=status_code,
            retryable=True,
            safe_to_retry=safe_to_retry,
            details=details,
            fields=fields,
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
            retryable=True,
            safe_to_retry=safe_to_retry,
            details=details,
        )


class TimeoutError(NetworkError):
    """The request exceeded the configured timeout."""


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
    """Create the public error subtype corresponding to an HTTP status."""
    arguments: _ErrorContext = {
        "code": code,
        "request_id": request_id,
        "status_code": status_code,
        "details": details,
        "fields": fields,
        "safe_to_retry": safe_to_retry,
    }
    if status_code in {401, 403}:
        return AuthenticationError(message, **arguments)
    if status_code == 404:
        return NotFoundError(message, **arguments)
    if status_code == 409:
        return ConflictError(message, **arguments)
    if status_code == 429:
        return RateLimitError(message, retry_after=retry_after, **arguments)
    if status_code in {400, 422}:
        return ValidationError(message, **arguments)
    if status_code >= 500:
        return ServerError(message, **arguments)
    return FrontalError(message, **arguments)


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

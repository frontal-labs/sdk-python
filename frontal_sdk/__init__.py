"""Python client library for the Frontal API."""

from frontal_sdk.client import AsyncFrontal, Frontal
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
from frontal_sdk.core.pagination import async_paginate, paginate
from frontal_sdk.core.polling import async_poll_until, poll_until
from frontal_sdk.models import (
    APIModel,
    ErrorField,
    ErrorResponse,
    JSONDocument,
    JSONObject,
    JSONPrimitive,
    JSONValue,
    MultipartPart,
    PageResult,
    PaginationMeta,
    QueryParams,
    RequestBody,
    ServerEvent,
)

__version__ = "1.0.0"

__all__ = [
    "APIModel",
    "AsyncFrontal",
    "async_paginate",
    "async_poll_until",
    "AuthenticationError",
    "ClientConfig",
    "ConflictError",
    "ErrorField",
    "ErrorResponse",
    "Frontal",
    "FrontalError",
    "JSONDocument",
    "JSONObject",
    "JSONPrimitive",
    "JSONValue",
    "MultipartPart",
    "NetworkError",
    "NotFoundError",
    "PageResult",
    "paginate",
    "PaginationMeta",
    "poll_until",
    "QueryParams",
    "RateLimitError",
    "RequestBody",
    "ServerError",
    "ServerEvent",
    "TimeoutError",
    "ValidationError",
    "__version__",
]

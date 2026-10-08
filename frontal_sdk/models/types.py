"""Pydantic-backed JSON values used at the Frontal API boundary."""

from __future__ import annotations

from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, Field, JsonValue, RootModel

# Pydantic evaluates model fields on Python 3.9, where `str | None` is unsupported.
JSONPrimitive = Union[str, int, float, bool, None]
JSONValue = JsonValue
JSONObject = dict[str, JSONValue]


class APIModel(BaseModel):
    """Base class for request and response models supplied by the SDK."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class JSONDocument(RootModel[JSONValue]):
    """Validated JSON payload for operations without a published schema."""


class ErrorField(APIModel):
    """A field-level validation issue returned by the API."""

    field: str
    message: str
    code: Optional[str] = None  # noqa: UP045


class ErrorResponse(APIModel):
    """Common structured API error envelope."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    code: Optional[str] = None  # noqa: UP045
    message: str = "API request failed"
    request_id: Optional[str] = Field(default=None, alias="requestId")  # noqa: UP045
    docs: Optional[str] = None  # noqa: UP045
    fields: list[ErrorField] = Field(default_factory=list)
    details: JSONValue = None


__all__ = [
    "APIModel",
    "ErrorField",
    "ErrorResponse",
    "JSONDocument",
    "JSONObject",
    "JSONPrimitive",
    "JSONValue",
]

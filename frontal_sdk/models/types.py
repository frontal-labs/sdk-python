"""Pydantic-backed JSON values used at the Frontal API boundary."""

from __future__ import annotations

from typing import Union

from pydantic import BaseModel, ConfigDict, Field, JsonValue, RootModel

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
    code: str | None = None


class ErrorResponse(APIModel):
    """Common structured API error envelope."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    code: str | None = None
    message: str = "API request failed"
    request_id: str | None = Field(default=None, alias="requestId")
    docs: str | None = None
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

"""Typed values used by the HTTP transport."""

from __future__ import annotations

from dataclasses import dataclass

from frontal_sdk.models.types import JSONValue


@dataclass(frozen=True)
class MultipartPart:
    """One file field in a multipart request."""

    name: str
    data: bytes
    filename: str
    content_type: str = "application/octet-stream"


@dataclass(frozen=True)
class ServerEvent:
    """A parsed server-sent event frame."""

    event: str
    data: JSONValue
    id: str | None

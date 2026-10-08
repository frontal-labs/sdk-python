"""Structured errors returned by the Frontal API."""

from __future__ import annotations

from frontal_sdk.api_types import JSONValue


class FrontalError(Exception):
    """An HTTP or protocol error from the Frontal API."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        code: str | None = None,
        request_id: str | None = None,
        details: JSONValue = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.request_id = request_id
        self.details = details

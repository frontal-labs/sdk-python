"""Typed API resource for the audit endpoints."""

from __future__ import annotations

from typing import Generic

from frontal_sdk.core.operation import Operation
from frontal_sdk.models import QueryParams, RequestBody
from frontal_sdk.resources._base import (
    APIResource,
    BytesResultT,
    JSONResultT,
    StreamResultT,
)


class Audit(
    APIResource[JSONResultT, BytesResultT, StreamResultT],
    Generic[JSONResultT, BytesResultT, StreamResultT],
):
    """Methods for the audit API endpoints."""

    def get_audit_events(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /audit/events."""
        return self._request(
            Operation("GET", "/audit/events"),
            path_params=(),
            query=query,
        )

    def get_audit_events_by_param_1(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /audit/events/{param}."""
        return self._request(
            Operation("GET", "/audit/events/{param}"),
            path_params=(param_1,),
            query=query,
        )

    def post_audit_events(
        self, *, query: QueryParams | None = None, body: RequestBody = None
    ) -> JSONResultT:
        """Call POST /audit/events."""
        return self._request(
            Operation("POST", "/audit/events"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_audit_events_batch(
        self, *, query: QueryParams | None = None, body: RequestBody = None
    ) -> JSONResultT:
        """Call POST /audit/events/batch."""
        return self._request(
            Operation("POST", "/audit/events/batch"),
            path_params=(),
            query=query,
            body=body,
        )

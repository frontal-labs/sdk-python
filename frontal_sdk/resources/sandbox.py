"""Typed API resource for the sandbox endpoints."""

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


class Sandbox(
    APIResource[JSONResultT, BytesResultT, StreamResultT],
    Generic[JSONResultT, BytesResultT, StreamResultT],
):
    """Methods for the sandbox API endpoints."""

    def get_sandbox_languages(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /sandbox/languages."""
        return self._request(
            Operation("GET", "/sandbox/languages"),
            path_params=(),
            query=query,
        )

    def post_sandbox_self_test(
        self, *, query: QueryParams | None = None, body: RequestBody = None
    ) -> JSONResultT:
        """Call POST /sandbox/self-test."""
        return self._request(
            Operation("POST", "/sandbox/self-test"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_sandbox_submit(
        self, *, query: QueryParams | None = None, body: RequestBody = None
    ) -> JSONResultT:
        """Call POST /sandbox/submit."""
        return self._request(
            Operation("POST", "/sandbox/submit"),
            path_params=(),
            query=query,
            body=body,
        )

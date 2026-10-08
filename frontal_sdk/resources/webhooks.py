"""Typed API resource for the webhooks endpoints."""

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


class Webhooks(
    APIResource[JSONResultT, BytesResultT, StreamResultT],
    Generic[JSONResultT, BytesResultT, StreamResultT],
):
    """Methods for the webhooks API endpoints."""

    def delete_webhooks_by_param_1(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /webhooks/{param}."""
        return self._request(
            Operation("DELETE", "/webhooks/{param}"),
            path_params=(param_1,),
            query=query,
        )

    def get_webhooks(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /webhooks."""
        return self._request(
            Operation("GET", "/webhooks"),
            path_params=(),
            query=query,
        )

    def get_webhooks_by_param_1(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /webhooks/{param}."""
        return self._request(
            Operation("GET", "/webhooks/{param}"),
            path_params=(param_1,),
            query=query,
        )

    def get_webhooks_deliveries(
        self, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /webhooks/deliveries."""
        return self._request(
            Operation("GET", "/webhooks/deliveries"),
            path_params=(),
            query=query,
        )

    def get_webhooks_deliveries_by_param_1(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /webhooks/deliveries/{param}."""
        return self._request(
            Operation("GET", "/webhooks/deliveries/{param}"),
            path_params=(param_1,),
            query=query,
        )

    def get_webhooks_stats(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /webhooks/stats."""
        return self._request(
            Operation("GET", "/webhooks/stats"),
            path_params=(),
            query=query,
        )

    def post_webhooks(
        self, *, query: QueryParams | None = None, body: RequestBody = None
    ) -> JSONResultT:
        """Call POST /webhooks."""
        return self._request(
            Operation("POST", "/webhooks"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_webhooks_by_param_1_rotate_secret(
        self,
        param_1: str,
        *,
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONResultT:
        """Call POST /webhooks/{param}/rotate-secret."""
        return self._request(
            Operation("POST", "/webhooks/{param}/rotate-secret"),
            path_params=(param_1,),
            query=query,
            body=body,
        )

    def post_webhooks_deliveries_by_param_1_retry(
        self,
        param_1: str,
        *,
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONResultT:
        """Call POST /webhooks/deliveries/{param}/retry."""
        return self._request(
            Operation("POST", "/webhooks/deliveries/{param}/retry"),
            path_params=(param_1,),
            query=query,
            body=body,
        )

    def put_webhooks_by_param_1(
        self,
        param_1: str,
        *,
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONResultT:
        """Call PUT /webhooks/{param}."""
        return self._request(
            Operation("PUT", "/webhooks/{param}"),
            path_params=(param_1,),
            query=query,
            body=body,
        )

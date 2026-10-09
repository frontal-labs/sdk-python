"""Typed API resource for the webhooks endpoints."""

from __future__ import annotations

from typing import Generic

from frontal_sdk.core.operation import Operation
from frontal_sdk.models import QueryParams
from frontal_sdk.models.requests import UNSET, RequestBodyInput
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

    def delete_webhook(
        self, webhook_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /webhooks/{param}."""
        return self._request(
            Operation("DELETE", "/webhooks/{param}"),
            path_params=(webhook_id,),
            query=query,
        )

    def list_webhooks(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /webhooks."""
        return self._request(
            Operation("GET", "/webhooks"),
            path_params=(),
            query=query,
        )

    def get_webhook(
        self, webhook_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /webhooks/{param}."""
        return self._request(
            Operation("GET", "/webhooks/{param}"),
            path_params=(webhook_id,),
            query=query,
        )

    def list_deliveries(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /webhooks/deliveries."""
        return self._request(
            Operation("GET", "/webhooks/deliveries"),
            path_params=(),
            query=query,
        )

    def get_delivery(
        self, delivery_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /webhooks/deliveries/{param}."""
        return self._request(
            Operation("GET", "/webhooks/deliveries/{param}"),
            path_params=(delivery_id,),
            query=query,
        )

    def list_stats(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /webhooks/stats."""
        return self._request(
            Operation("GET", "/webhooks/stats"),
            path_params=(),
            query=query,
        )

    def create_webhook(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /webhooks."""
        return self._request(
            Operation("POST", "/webhooks"),
            path_params=(),
            query=query,
            body=body,
        )

    def rotate_secret_webhook(
        self,
        webhook_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /webhooks/{param}/rotate-secret."""
        return self._request(
            Operation("POST", "/webhooks/{param}/rotate-secret"),
            path_params=(webhook_id,),
            query=query,
            body=body,
        )

    def retry_delivery(
        self,
        delivery_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /webhooks/deliveries/{param}/retry."""
        return self._request(
            Operation("POST", "/webhooks/deliveries/{param}/retry"),
            path_params=(delivery_id,),
            query=query,
            body=body,
        )

    def update_webhook(
        self,
        webhook_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call PUT /webhooks/{param}."""
        return self._request(
            Operation("PUT", "/webhooks/{param}"),
            path_params=(webhook_id,),
            query=query,
            body=body,
        )

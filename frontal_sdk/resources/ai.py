"""Typed API resource for the ai endpoints."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Generic

from frontal_sdk.core.operation import Operation
from frontal_sdk.models import MultipartPart, QueryParams, RequestBody
from frontal_sdk.resources._base import (
    APIResource,
    BytesResultT,
    JSONResultT,
    StreamResultT,
)


class AI(
    APIResource[JSONResultT, BytesResultT, StreamResultT],
    Generic[JSONResultT, BytesResultT, StreamResultT],
):
    """Methods for the ai API endpoints."""

    def get_health(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /health."""
        return self._request(
            Operation("GET", "/health"),
            path_params=(),
            query=query,
        )

    def get_internal_models(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /internal/models."""
        return self._request(
            Operation("GET", "/internal/models"),
            path_params=(),
            query=query,
        )

    def get_internal_models_defaults(
        self, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /internal/models/defaults."""
        return self._request(
            Operation("GET", "/internal/models/defaults"),
            path_params=(),
            query=query,
        )

    def post_ai_chat_completions(
        self, *, query: QueryParams | None = None, body: RequestBody = None
    ) -> JSONResultT:
        """Call POST /ai/chat/completions."""
        return self._request(
            Operation("POST", "/ai/chat/completions"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_internal_embeddings(
        self, *, query: QueryParams | None = None, body: RequestBody = None
    ) -> JSONResultT:
        """Call POST /internal/embeddings."""
        return self._request(
            Operation("POST", "/internal/embeddings"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_internal_predictions(
        self, *, query: QueryParams | None = None, body: RequestBody = None
    ) -> JSONResultT:
        """Call POST /internal/predictions."""
        return self._request(
            Operation("POST", "/internal/predictions"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_internal_rerank(
        self, *, query: QueryParams | None = None, body: RequestBody = None
    ) -> JSONResultT:
        """Call POST /internal/rerank."""
        return self._request(
            Operation("POST", "/internal/rerank"),
            path_params=(),
            query=query,
            body=body,
        )

    def upload_internal_predictions(
        self, parts: Sequence[MultipartPart], *, fields: Mapping[str, str] | None = None
    ) -> JSONResultT:
        """Call POSTFORMDATA /internal/predictions."""
        return self._upload(
            Operation("POSTFORMDATA", "/internal/predictions"),
            parts,
            path_params=(),
            fields=fields,
        )

    def post_raw_internal_predictions(
        self, data: bytes, content_type: str, *, query: QueryParams | None = None
    ) -> BytesResultT:
        """Call POSTRAW /internal/predictions."""
        return self._post_raw(
            Operation("POSTRAW", "/internal/predictions"),
            data,
            content_type,
            path_params=(),
            query=query,
        )

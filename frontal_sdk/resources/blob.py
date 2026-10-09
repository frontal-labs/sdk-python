"""Typed API resource for the blob endpoints."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Generic

from frontal_sdk.core.operation import Operation
from frontal_sdk.models import MultipartPart, QueryParams
from frontal_sdk.models.requests import UNSET, RequestBodyInput
from frontal_sdk.resources._base import (
    APIResource,
    BytesResultT,
    JSONResultT,
    StreamResultT,
)


class Blob(
    APIResource[JSONResultT, BytesResultT, StreamResultT],
    Generic[JSONResultT, BytesResultT, StreamResultT],
):
    """Methods for the blob API endpoints."""

    def delete_object(
        self, container: str, object_key: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /blob/object/{param}/{param}."""
        return self._request(
            Operation("DELETE", "/blob/object/{param}/{param}"),
            path_params=(container, object_key),
            query=query,
        )

    def get_object_info(
        self, container: str, object_key: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /blob/object/info/{param}/{param}."""
        return self._request(
            Operation("GET", "/blob/object/info/{param}/{param}"),
            path_params=(container, object_key),
            query=query,
        )

    def get_object(
        self, container: str, object_key: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /blob/object/{param}/{param}."""
        return self._request(
            Operation("GET", "/blob/object/{param}/{param}"),
            path_params=(container, object_key),
            query=query,
        )

    def post_blob_object_copy(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /blob/object/copy."""
        return self._request(
            Operation("POST", "/blob/object/copy"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_blob_object_list_by_list_id(
        self,
        list_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /blob/object/list/{param}."""
        return self._request(
            Operation("POST", "/blob/object/list/{param}"),
            path_params=(list_id,),
            query=query,
            body=body,
        )

    def post_blob_object_move(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /blob/object/move."""
        return self._request(
            Operation("POST", "/blob/object/move"),
            path_params=(),
            query=query,
            body=body,
        )

    def sign_object(
        self,
        container: str,
        object_key: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /blob/object/sign/{param}/{param}."""
        return self._request(
            Operation("POST", "/blob/object/sign/{param}/{param}"),
            path_params=(container, object_key),
            query=query,
            body=body,
        )

    def upload_object(
        self,
        container: str,
        object_key: str,
        parts: Sequence[MultipartPart],
        *,
        fields: Mapping[str, str] | None = None,
    ) -> JSONResultT:
        """Call POSTFORMDATA /blob/object/{param}/{param}."""
        return self._upload(
            Operation("POSTFORMDATA", "/blob/object/{param}/{param}"),
            parts,
            path_params=(container, object_key),
            fields=fields,
        )

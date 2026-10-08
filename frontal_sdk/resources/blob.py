"""Typed API resource for the blob endpoints."""

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


class Blob(
    APIResource[JSONResultT, BytesResultT, StreamResultT],
    Generic[JSONResultT, BytesResultT, StreamResultT],
):
    """Methods for the blob API endpoints."""

    def delete_blob_object_by_param_1_by_param_2(
        self, param_1: str, param_2: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /blob/object/{param}/{param}."""
        return self._request(
            Operation("DELETE", "/blob/object/{param}/{param}"),
            path_params=(param_1, param_2),
            query=query,
        )

    def get_blob_object_info_by_param_1_by_param_2(
        self, param_1: str, param_2: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /blob/object/info/{param}/{param}."""
        return self._request(
            Operation("GET", "/blob/object/info/{param}/{param}"),
            path_params=(param_1, param_2),
            query=query,
        )

    def get_blob_object_by_param_1_by_param_2(
        self, param_1: str, param_2: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /blob/object/{param}/{param}."""
        return self._request(
            Operation("GET", "/blob/object/{param}/{param}"),
            path_params=(param_1, param_2),
            query=query,
        )

    def post_blob_object_copy(
        self, *, query: QueryParams | None = None, body: RequestBody = None
    ) -> JSONResultT:
        """Call POST /blob/object/copy."""
        return self._request(
            Operation("POST", "/blob/object/copy"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_blob_object_list_by_param_1(
        self,
        param_1: str,
        *,
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONResultT:
        """Call POST /blob/object/list/{param}."""
        return self._request(
            Operation("POST", "/blob/object/list/{param}"),
            path_params=(param_1,),
            query=query,
            body=body,
        )

    def post_blob_object_move(
        self, *, query: QueryParams | None = None, body: RequestBody = None
    ) -> JSONResultT:
        """Call POST /blob/object/move."""
        return self._request(
            Operation("POST", "/blob/object/move"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_blob_object_sign_by_param_1_by_param_2(
        self,
        param_1: str,
        param_2: str,
        *,
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONResultT:
        """Call POST /blob/object/sign/{param}/{param}."""
        return self._request(
            Operation("POST", "/blob/object/sign/{param}/{param}"),
            path_params=(param_1, param_2),
            query=query,
            body=body,
        )

    def upload_blob_object_by_param_1_by_param_2(
        self,
        param_1: str,
        param_2: str,
        parts: Sequence[MultipartPart],
        *,
        fields: Mapping[str, str] | None = None,
    ) -> JSONResultT:
        """Call POSTFORMDATA /blob/object/{param}/{param}."""
        return self._upload(
            Operation("POSTFORMDATA", "/blob/object/{param}/{param}"),
            parts,
            path_params=(param_1, param_2),
            fields=fields,
        )

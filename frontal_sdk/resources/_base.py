"""Shared operation dispatch for generated resource classes."""

from __future__ import annotations

from collections.abc import Iterator, Mapping, Sequence

from frontal_sdk.core.http import HttpClient
from frontal_sdk.core.operation import Operation
from frontal_sdk.models import JSONValue, MultipartPart, QueryParams, ServerEvent


class APIResource:
    """Base class for resource groups backed by the shared HTTP client."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def _request(
        self,
        operation: Operation,
        *,
        path_params: Sequence[str] = (),
        query: QueryParams | None = None,
        body: JSONValue = None,
    ) -> JSONValue:
        return self._http.request(
            operation, path_params=path_params, query=query, body=body
        )

    def _upload(
        self,
        operation: Operation,
        parts: Sequence[MultipartPart],
        *,
        path_params: Sequence[str] = (),
        fields: Mapping[str, str] | None = None,
    ) -> JSONValue:
        return self._http.request_multipart(
            operation, parts, path_params=path_params, fields=fields
        )

    def _post_raw(
        self,
        operation: Operation,
        data: bytes,
        content_type: str,
        *,
        path_params: Sequence[str] = (),
        query: QueryParams | None = None,
    ) -> bytes:
        return self._http.request_raw(
            operation,
            data,
            content_type,
            path_params=path_params,
            query=query,
        )

    def _request_bytes(
        self,
        operation: Operation,
        *,
        path_params: Sequence[str] = (),
        query: QueryParams | None = None,
    ) -> bytes:
        return self._http.request_bytes(operation, path_params=path_params, query=query)

    def _stream(
        self,
        operation: Operation,
        *,
        path_params: Sequence[str] = (),
        query: QueryParams | None = None,
    ) -> Iterator[ServerEvent]:
        return self._http.stream(operation, path_params=path_params, query=query)

"""Shared transport protocol for typed resource groups."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Generic, Protocol, TypeVar

from frontal_sdk.core.operation import Operation
from frontal_sdk.models import MultipartPart, QueryParams, RequestBody

JSONResultT = TypeVar("JSONResultT", covariant=True)
BytesResultT = TypeVar("BytesResultT", covariant=True)
StreamResultT = TypeVar("StreamResultT", covariant=True)


class HTTPTransport(Protocol[JSONResultT, BytesResultT, StreamResultT]):
    """Operations shared by synchronous and asynchronous transports."""

    def request(
        self,
        operation: Operation,
        *,
        path_params: Sequence[str] = (),
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONResultT: ...

    def request_multipart(
        self,
        operation: Operation,
        parts: Sequence[MultipartPart],
        *,
        path_params: Sequence[str] = (),
        fields: Mapping[str, str] | None = None,
    ) -> JSONResultT: ...

    def request_raw(
        self,
        operation: Operation,
        data: bytes,
        content_type: str,
        *,
        path_params: Sequence[str] = (),
        query: QueryParams | None = None,
    ) -> BytesResultT: ...

    def request_bytes(
        self,
        operation: Operation,
        *,
        path_params: Sequence[str] = (),
        query: QueryParams | None = None,
    ) -> BytesResultT: ...

    def stream(
        self,
        operation: Operation,
        *,
        path_params: Sequence[str] = (),
        query: QueryParams | None = None,
    ) -> StreamResultT: ...


class APIResource(Generic[JSONResultT, BytesResultT, StreamResultT]):
    """Base class for API resource groups backed by a shared transport."""

    def __init__(
        self,
        http: HTTPTransport[JSONResultT, BytesResultT, StreamResultT],
    ) -> None:
        self._http = http

    def _request(
        self,
        operation: Operation,
        *,
        path_params: Sequence[str] = (),
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONResultT:
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
    ) -> JSONResultT:
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
    ) -> BytesResultT:
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
    ) -> BytesResultT:
        return self._http.request_bytes(operation, path_params=path_params, query=query)

    def _stream(
        self,
        operation: Operation,
        *,
        path_params: Sequence[str] = (),
        query: QueryParams | None = None,
    ) -> StreamResultT:
        return self._http.stream(operation, path_params=path_params, query=query)

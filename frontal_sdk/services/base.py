"""Common implementation for generated service endpoint groups."""

from __future__ import annotations

from collections.abc import Iterator, Mapping, Sequence
from typing import Generic, TypeVar

from frontal_sdk.api_types import JSONValue
from frontal_sdk.utils.http import HttpClient, MultipartPart, ServerEvent
from frontal_sdk.utils.operation import Endpoint

E = TypeVar("E", bound=Endpoint)


class BaseServiceClient(Generic[E]):
    """Provides shared transport operations to generated service clients."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def call(
        self,
        endpoint: E,
        *,
        path_params: Sequence[str] = (),
        query: Mapping[str, str | int | float | bool] | None = None,
        body: JSONValue = None,
    ) -> JSONValue:
        return self._http.request(
            endpoint.operation,
            path_params=path_params,
            query=query,
            body=body,
        )

    def upload(
        self,
        endpoint: E,
        parts: Sequence[MultipartPart],
        *,
        path_params: Sequence[str] = (),
        fields: Mapping[str, str] | None = None,
    ) -> JSONValue:
        return self._http.request_multipart(
            endpoint.operation,
            parts,
            path_params=path_params,
            fields=fields,
        )

    def post_raw(
        self,
        endpoint: E,
        data: bytes,
        content_type: str,
        *,
        path_params: Sequence[str] = (),
        query: Mapping[str, str | int | float | bool] | None = None,
    ) -> bytes:
        return self._http.request_raw(
            endpoint.operation,
            data,
            content_type,
            path_params=path_params,
            query=query,
        )

    def request_bytes(
        self,
        endpoint: E,
        *,
        path_params: Sequence[str] = (),
        query: Mapping[str, str | int | float | bool] | None = None,
    ) -> bytes:
        return self._http.request_bytes(
            endpoint.operation,
            path_params=path_params,
            query=query,
        )

    def stream(
        self,
        endpoint: E,
        *,
        path_params: Sequence[str] = (),
        query: Mapping[str, str | int | float | bool] | None = None,
    ) -> Iterator[ServerEvent]:
        return self._http.stream(
            endpoint.operation,
            path_params=path_params,
            query=query,
        )

"""Synchronous and asynchronous HTTPX transports for the Frontal API."""

from __future__ import annotations

import json
import logging
from collections.abc import AsyncIterator, Coroutine, Iterator, Mapping, Sequence
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from math import isfinite
from typing import Any, cast
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from uuid import uuid4

import anyio
import httpx
from pydantic import BaseModel, TypeAdapter
from pydantic import ValidationError as PydanticValidationError

from frontal_sdk.core.config import ClientConfig
from frontal_sdk.core.errors import (
    FrontalError,
    NetworkError,
    TimeoutError,
    error_for_status,
)
from frontal_sdk.core.operation import Operation
from frontal_sdk.models import (
    ErrorField,
    ErrorResponse,
    JSONValue,
    MultipartPart,
    QueryParams,
)
from frontal_sdk.models.http import ServerEvent
from frontal_sdk.models.requests import RequestBody

_RETRYABLE_STATUS = {408, 425, 429, 500, 502, 503, 504}
_JSON_ADAPTER: TypeAdapter[JSONValue] = TypeAdapter(JSONValue)
_LOGGER = logging.getLogger("frontal_sdk.http")


def _request_url(
    base_url: str,
    operation: Operation,
    path_params: Sequence[str],
    query: QueryParams | None,
) -> str:
    path = operation.render_path(tuple(path_params))
    fixed = urlsplit(path)
    base = urlsplit(base_url)
    query_items = parse_qsl(fixed.query, keep_blank_values=True)
    if query:
        query_items.extend((key, str(value)) for key, value in query.items())
    return urlunsplit(
        (
            base.scheme,
            base.netloc,
            f"{base.path.rstrip('/')}{fixed.path}",
            urlencode(query_items),
            "",
        )
    )


def _json_body(body: RequestBody) -> JSONValue:
    if isinstance(body, BaseModel):
        body = cast(JSONValue, body.model_dump(mode="json", by_alias=True))
    try:
        return _JSON_ADAPTER.validate_python(body)
    except PydanticValidationError as error:
        raise ValueError("request body must contain JSON-compatible values") from error


def _headers(
    config: ClientConfig, extra: Mapping[str, str] | None = None
) -> dict[str, str]:
    values = {
        "Authorization": f"Bearer {config.api_key}",
        "Accept": "application/json",
        "User-Agent": "frontal-python-sdk/1.0.0",
        "X-Request-ID": str(uuid4()),
        "X-Frontal-Environment": config.environment,
        **config.headers,
        **(extra or {}),
    }
    return values


def _api_error(response: httpx.Response) -> FrontalError:
    request_id = response.headers.get("x-request-id")
    code: str | None = None
    message = f"Frontal API request failed with HTTP {response.status_code}"
    details: JSONValue = None
    fields: list[ErrorField] = []
    try:
        decoded = response.json()
    except (ValueError, UnicodeDecodeError):
        decoded = None
    if isinstance(decoded, dict):
        try:
            envelope = ErrorResponse.model_validate(decoded)
        except PydanticValidationError:
            pass
        else:
            code = envelope.code
            message = envelope.message
            request_id = envelope.request_id or request_id
            details = envelope.details
            fields = envelope.fields
    else:
        fields = []
        if response.content:
            details = response.text[:2048]

    return error_for_status(
        response.status_code,
        message,
        code=code,
        request_id=request_id,
        details=details,
        fields=fields,
        retry_after=_parse_retry_after(response.headers.get("retry-after")),
    )


def _decode_json(response: httpx.Response) -> JSONValue:
    if not response.content:
        return None
    content_type = response.headers.get("content-type", "").split(";", 1)[0].strip()
    if content_type != "application/json" and not content_type.endswith("+json"):
        raise FrontalError(
            "Expected JSON response, received "
            f"{content_type or 'unknown content type'}",
            request_id=response.headers.get("x-request-id"),
            status_code=response.status_code,
        )
    try:
        return _JSON_ADAPTER.validate_python(response.json())
    except (ValueError, PydanticValidationError) as error:
        raise FrontalError(
            "The API returned invalid JSON",
            request_id=response.headers.get("x-request-id"),
            status_code=response.status_code,
        ) from error


def _parse_retry_after(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        seconds = float(value)
        if isfinite(seconds):
            return min(max(seconds, 0.0), 5.0)
    except ValueError:
        pass
    try:
        when = parsedate_to_datetime(value)
        if when.tzinfo is None:
            when = when.replace(tzinfo=timezone.utc)
        return min(max((when - datetime.now(timezone.utc)).total_seconds(), 0.0), 5.0)
    except (TypeError, ValueError, OverflowError):
        return None


def _retry_delay(attempt: int, retry_after: float | None) -> float:
    if retry_after is not None:
        return retry_after
    return float(min(0.1 * (2**attempt), 2.0))


def _event(event: str, event_id: str | None, lines: list[str]) -> ServerEvent:
    payload = "\n".join(lines)
    try:
        data = _JSON_ADAPTER.validate_python(json.loads(payload))
    except (ValueError, PydanticValidationError):
        data = payload
    return ServerEvent(event, data, event_id)


def _parse_event_line(
    line: str,
    event: str,
    event_id: str | None,
    data_lines: list[str],
) -> tuple[str, str | None, list[str], ServerEvent | None]:
    if not line:
        parsed_event = _event(event, event_id, data_lines) if data_lines else None
        return "message", None, [], parsed_event
    if line.startswith(":"):
        return event, event_id, data_lines, None
    if ":" not in line:
        field, value = line, ""
    else:
        field, value = line.split(":", 1)
        if value.startswith(" "):
            value = value[1:]
    if field == "event":
        return value or "message", event_id, data_lines, None
    if field == "id" and "\0" not in value:
        return event, value, data_lines, None
    if field == "data":
        return event, event_id, [*data_lines, value], None
    return event, event_id, data_lines, None


class HttpClient:
    """Synchronous HTTPX transport shared by every service on a client."""

    def __init__(
        self, config: ClientConfig, client: httpx.Client | None = None
    ) -> None:
        self._config = config
        self._client = client or httpx.Client(timeout=config.timeout)
        self._owns_client = client is None

    def request(
        self,
        operation: Operation,
        *,
        path_params: Sequence[str] = (),
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONValue:
        """Call one catalogued operation and validate the JSON response."""
        if operation.method in {"GETRAW", "STREAM", "POSTFORMDATA", "POSTRAW"}:
            raise ValueError(
                "use request_bytes(), stream(), request_multipart(), or request_raw()"
            )
        url = _request_url(self._config.base_url, operation, path_params, query)
        content = (
            _json_body(body)
            if body is not None
            else {}
            if operation.method in {"POST", "PUT", "PATCH", "DELETE"}
            else None
        )
        headers = _headers(
            self._config,
            {"Content-Type": "application/json"} if content is not None else None,
        )
        request = self._client.build_request(
            operation.method,
            url,
            headers=headers,
            json=content,
        )
        response = self._send(request, operation.method)
        return _decode_json(response)

    def request_multipart(
        self,
        operation: Operation,
        parts: Sequence[MultipartPart],
        *,
        path_params: Sequence[str] = (),
        fields: Mapping[str, str] | None = None,
    ) -> JSONValue:
        """Send a multipart file upload to a POSTFORMDATA operation."""
        if operation.method != "POSTFORMDATA":
            raise ValueError("request_multipart() requires POSTFORMDATA")
        files = [
            (part.name, (part.filename, part.data, part.content_type)) for part in parts
        ]
        request = self._client.build_request(
            "POST",
            _request_url(self._config.base_url, operation, path_params, None),
            headers=_headers(self._config),
            data=fields or {},
            files=files,
        )
        return _decode_json(self._send(request, "POST"))

    def request_raw(
        self,
        operation: Operation,
        data: bytes,
        content_type: str,
        *,
        path_params: Sequence[str] = (),
        query: QueryParams | None = None,
    ) -> bytes:
        """Send raw bytes to a POSTRAW operation and return response bytes."""
        if operation.method != "POSTRAW":
            raise ValueError("request_raw() requires POSTRAW")
        request = self._client.build_request(
            "POST",
            _request_url(self._config.base_url, operation, path_params, query),
            headers=_headers(self._config, {"Content-Type": content_type}),
            content=data,
        )
        return self._send(request, "POST").content

    def request_bytes(
        self,
        operation: Operation,
        *,
        path_params: Sequence[str] = (),
        query: QueryParams | None = None,
    ) -> bytes:
        """Read a successful non-streaming response without JSON decoding."""
        if operation.method in {"STREAM", "POSTFORMDATA", "POSTRAW"}:
            raise ValueError("use stream(), request_multipart(), or request_raw()")
        method = "GET" if operation.method == "GETRAW" else operation.method
        request = self._client.build_request(
            method,
            _request_url(self._config.base_url, operation, path_params, query),
            headers=_headers(self._config, {"Accept": "*/*"}),
        )
        return self._send(request, method).content

    def stream(
        self,
        operation: Operation,
        *,
        path_params: Sequence[str] = (),
        query: QueryParams | None = None,
    ) -> Iterator[ServerEvent]:
        """Yield parsed SSE events and close the response when iteration ends."""
        if operation.method != "STREAM":
            raise ValueError("stream() requires a STREAM operation")
        url = _request_url(self._config.base_url, operation, path_params, query)
        attempt = 0
        while True:
            try:
                with self._client.stream(
                    "GET",
                    url,
                    headers=_headers(self._config, {"Accept": "text/event-stream"}),
                ) as response:
                    if (
                        response.status_code in _RETRYABLE_STATUS
                        and attempt < self._config.max_retries
                    ):
                        delay = _retry_delay(
                            attempt,
                            _parse_retry_after(response.headers.get("retry-after")),
                        )
                        time_sleep(delay)
                        attempt += 1
                        continue
                    if response.is_error:
                        raise _api_error(response)
                    if not response.headers.get("content-type", "").startswith(
                        "text/event-stream"
                    ):
                        raise FrontalError(
                            "The API did not return an event stream",
                            request_id=response.headers.get("x-request-id"),
                            status_code=response.status_code,
                        )
                    event = "message"
                    event_id: str | None = None
                    data_lines: list[str] = []
                    for line in response.iter_lines():
                        event, event_id, data_lines, parsed = _parse_event_line(
                            line, event, event_id, data_lines
                        )
                        if parsed is not None:
                            yield parsed
                    if data_lines:
                        yield _event(event, event_id, data_lines)
                    return
            except httpx.TimeoutException as error:
                if attempt < self._config.max_retries:
                    time_sleep(_retry_delay(attempt, None))
                    attempt += 1
                    continue
                raise TimeoutError(f"Stream request timed out: {error}") from error
            except httpx.RequestError as error:
                if attempt < self._config.max_retries:
                    time_sleep(_retry_delay(attempt, None))
                    attempt += 1
                    continue
                raise NetworkError(f"Stream request failed: {error}") from error

    def close(self) -> None:
        """Close the connection pool if this transport created it."""
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> HttpClient:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def _send(self, request: httpx.Request, method: str) -> httpx.Response:
        attempt = 0
        while True:
            try:
                if self._config.debug:
                    _LOGGER.debug("Frontal request %s %s", request.method, request.url)
                response = self._client.send(request)
                if (
                    method == "GET"
                    and response.status_code in _RETRYABLE_STATUS
                    and attempt < self._config.max_retries
                ):
                    time_sleep(
                        _retry_delay(
                            attempt,
                            _parse_retry_after(response.headers.get("retry-after")),
                        )
                    )
                    attempt += 1
                    continue
                if self._config.debug:
                    _LOGGER.debug(
                        "Frontal response %s request_id=%s",
                        response.status_code,
                        response.headers.get("x-request-id"),
                    )
                if response.is_error:
                    raise _api_error(response)
                return response
            except httpx.TimeoutException as error:
                if method == "GET" and attempt < self._config.max_retries:
                    time_sleep(_retry_delay(attempt, None))
                    attempt += 1
                    continue
                raise TimeoutError(f"Request timed out: {error}") from error
            except httpx.RequestError as error:
                if method == "GET" and attempt < self._config.max_retries:
                    time_sleep(_retry_delay(attempt, None))
                    attempt += 1
                    continue
                raise NetworkError(f"Request failed: {error}") from error


def time_sleep(delay: float) -> None:
    """Sync backoff hook kept separate for deterministic transport tests."""
    import time

    time.sleep(delay)


class AsyncHttpClient:
    """Asynchronous HTTPX transport shared by every async service."""

    def __init__(
        self,
        config: ClientConfig,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self._config = config
        self._client = client or httpx.AsyncClient(timeout=config.timeout)
        self._owns_client = client is None

    def request(
        self,
        operation: Operation,
        *,
        path_params: Sequence[str] = (),
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> Coroutine[Any, Any, JSONValue]:
        """Call one catalogued operation and validate the JSON response."""
        return self._request(operation, path_params=path_params, query=query, body=body)

    async def _request(
        self,
        operation: Operation,
        *,
        path_params: Sequence[str],
        query: QueryParams | None,
        body: RequestBody,
    ) -> JSONValue:
        if operation.method in {"GETRAW", "STREAM", "POSTFORMDATA", "POSTRAW"}:
            raise ValueError(
                "use request_bytes(), stream(), request_multipart(), or request_raw()"
            )
        content = (
            _json_body(body)
            if body is not None
            else {}
            if operation.method in {"POST", "PUT", "PATCH", "DELETE"}
            else None
        )
        headers = _headers(
            self._config,
            {"Content-Type": "application/json"} if content is not None else None,
        )
        request = self._client.build_request(
            operation.method,
            _request_url(self._config.base_url, operation, path_params, query),
            headers=headers,
            json=content,
        )
        response = await self._send(request, operation.method)
        return _decode_json(response)

    def request_multipart(
        self,
        operation: Operation,
        parts: Sequence[MultipartPart],
        *,
        path_params: Sequence[str] = (),
        fields: Mapping[str, str] | None = None,
    ) -> Coroutine[Any, Any, JSONValue]:
        """Send a multipart file upload to a POSTFORMDATA operation."""
        return self._request_multipart(
            operation, parts, path_params=path_params, fields=fields
        )

    async def _request_multipart(
        self,
        operation: Operation,
        parts: Sequence[MultipartPart],
        *,
        path_params: Sequence[str],
        fields: Mapping[str, str] | None,
    ) -> JSONValue:
        if operation.method != "POSTFORMDATA":
            raise ValueError("request_multipart() requires POSTFORMDATA")
        files = [
            (part.name, (part.filename, part.data, part.content_type)) for part in parts
        ]
        request = self._client.build_request(
            "POST",
            _request_url(self._config.base_url, operation, path_params, None),
            headers=_headers(self._config),
            data=fields or {},
            files=files,
        )
        return _decode_json(await self._send(request, "POST"))

    def request_raw(
        self,
        operation: Operation,
        data: bytes,
        content_type: str,
        *,
        path_params: Sequence[str] = (),
        query: QueryParams | None = None,
    ) -> Coroutine[Any, Any, bytes]:
        """Send raw bytes to a POSTRAW operation and return response bytes."""
        return self._request_raw(
            operation,
            data,
            content_type,
            path_params=path_params,
            query=query,
        )

    async def _request_raw(
        self,
        operation: Operation,
        data: bytes,
        content_type: str,
        *,
        path_params: Sequence[str],
        query: QueryParams | None,
    ) -> bytes:
        if operation.method != "POSTRAW":
            raise ValueError("request_raw() requires POSTRAW")
        request = self._client.build_request(
            "POST",
            _request_url(self._config.base_url, operation, path_params, query),
            headers=_headers(self._config, {"Content-Type": content_type}),
            content=data,
        )
        return (await self._send(request, "POST")).content

    def request_bytes(
        self,
        operation: Operation,
        *,
        path_params: Sequence[str] = (),
        query: QueryParams | None = None,
    ) -> Coroutine[Any, Any, bytes]:
        """Read a successful non-streaming response without JSON decoding."""
        return self._request_bytes(operation, path_params=path_params, query=query)

    async def _request_bytes(
        self,
        operation: Operation,
        *,
        path_params: Sequence[str],
        query: QueryParams | None,
    ) -> bytes:
        if operation.method in {"STREAM", "POSTFORMDATA", "POSTRAW"}:
            raise ValueError("use stream(), request_multipart(), or request_raw()")
        method = "GET" if operation.method == "GETRAW" else operation.method
        request = self._client.build_request(
            method,
            _request_url(self._config.base_url, operation, path_params, query),
            headers=_headers(self._config, {"Accept": "*/*"}),
        )
        return (await self._send(request, method)).content

    async def stream(
        self,
        operation: Operation,
        *,
        path_params: Sequence[str] = (),
        query: QueryParams | None = None,
    ) -> AsyncIterator[ServerEvent]:
        """Yield parsed SSE events and close the response when iteration ends."""
        if operation.method != "STREAM":
            raise ValueError("stream() requires a STREAM operation")
        url = _request_url(self._config.base_url, operation, path_params, query)
        attempt = 0
        while True:
            try:
                async with self._client.stream(
                    "GET",
                    url,
                    headers=_headers(self._config, {"Accept": "text/event-stream"}),
                ) as response:
                    if (
                        response.status_code in _RETRYABLE_STATUS
                        and attempt < self._config.max_retries
                    ):
                        await anyio.sleep(
                            _retry_delay(
                                attempt,
                                _parse_retry_after(response.headers.get("retry-after")),
                            )
                        )
                        attempt += 1
                        continue
                    if response.is_error:
                        raise _api_error(response)
                    if not response.headers.get("content-type", "").startswith(
                        "text/event-stream"
                    ):
                        raise FrontalError(
                            "The API did not return an event stream",
                            request_id=response.headers.get("x-request-id"),
                            status_code=response.status_code,
                        )
                    event = "message"
                    event_id: str | None = None
                    data_lines: list[str] = []
                    async for line in response.aiter_lines():
                        event, event_id, data_lines, parsed = _parse_event_line(
                            line, event, event_id, data_lines
                        )
                        if parsed is not None:
                            yield parsed
                    if data_lines:
                        yield _event(event, event_id, data_lines)
                    return
            except httpx.TimeoutException as error:
                if attempt < self._config.max_retries:
                    await anyio.sleep(_retry_delay(attempt, None))
                    attempt += 1
                    continue
                raise TimeoutError(f"Stream request timed out: {error}") from error
            except httpx.RequestError as error:
                if attempt < self._config.max_retries:
                    await anyio.sleep(_retry_delay(attempt, None))
                    attempt += 1
                    continue
                raise NetworkError(f"Stream request failed: {error}") from error

    async def aclose(self) -> None:
        """Close the connection pool if this transport created it."""
        if self._owns_client:
            await self._client.aclose()

    async def __aenter__(self) -> AsyncHttpClient:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.aclose()

    async def _send(self, request: httpx.Request, method: str) -> httpx.Response:
        attempt = 0
        while True:
            try:
                if self._config.debug:
                    _LOGGER.debug("Frontal request %s %s", request.method, request.url)
                response = await self._client.send(request)
                if (
                    method == "GET"
                    and response.status_code in _RETRYABLE_STATUS
                    and attempt < self._config.max_retries
                ):
                    await anyio.sleep(
                        _retry_delay(
                            attempt,
                            _parse_retry_after(response.headers.get("retry-after")),
                        )
                    )
                    attempt += 1
                    continue
                if self._config.debug:
                    _LOGGER.debug(
                        "Frontal response %s request_id=%s",
                        response.status_code,
                        response.headers.get("x-request-id"),
                    )
                if response.is_error:
                    raise _api_error(response)
                return response
            except httpx.TimeoutException as error:
                if method == "GET" and attempt < self._config.max_retries:
                    await anyio.sleep(_retry_delay(attempt, None))
                    attempt += 1
                    continue
                raise TimeoutError(f"Request timed out: {error}") from error
            except httpx.RequestError as error:
                if method == "GET" and attempt < self._config.max_retries:
                    await anyio.sleep(_retry_delay(attempt, None))
                    attempt += 1
                    continue
                raise NetworkError(f"Request failed: {error}") from error


__all__ = ["AsyncHttpClient", "HttpClient"]

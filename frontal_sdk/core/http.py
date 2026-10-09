"""Synchronous and asynchronous HTTPX transports for the Frontal API."""

from __future__ import annotations

import json
import logging
import random
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
from frontal_sdk.models.requests import UNSET, RequestBody, RequestBodyInput, Unset

_RETRYABLE_STATUS = {408, 425, 429, 500, 502, 503, 504}
_EVENT_STREAM_CONTENT_TYPE = "text/event-stream"
_EVENT_STREAM_ERROR = "The API did not return an event stream"
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


def _json_body_bytes(body: RequestBody) -> bytes:
    """Serialize a JSON value, including the valid top-level value ``null``."""
    return _JSON_ADAPTER.dump_json(_json_body(body))


def _request_body_bytes(body: RequestBodyInput) -> bytes | None:
    if isinstance(body, Unset):
        return None
    return _json_body_bytes(body)


def _headers(
    config: ClientConfig, extra: Mapping[str, str] | None = None
) -> dict[str, str]:
    values = {
        "Authorization": f"Bearer {config.api_key}",
        "Accept": "application/json",
        "User-Agent": "frontal-python-sdk/1.0.0",
        "X-Request-ID": str(uuid4()),
        "X-Frontal-Environment": config.environment,
    }
    # Header names are case-insensitive; normalize before merging to avoid
    # duplicate wire headers when callers vary the casing.
    for source in (config.headers, extra or {}):
        for name, value in source.items():
            existing = next(
                (key for key in values if key.lower() == name.lower()), None
            )
            if existing is not None:
                del values[existing]
            values[name] = value
    return values


def _decode_error_body(response: httpx.Response) -> Any:
    try:
        return response.json()
    except ValueError:
        return None


_ERROR_FIELDS = {
    "code",
    "message",
    "requestId",
    "request_id",
    "docs",
    "fields",
    "details",
}


def _error_envelope(
    decoded: dict[str, Any], response: httpx.Response, request_id: str | None
) -> tuple[str | None, str, str | None, JSONValue, list[ErrorField]]:
    code: str | None = None
    message = f"Frontal API request failed with HTTP {response.status_code}"
    details: JSONValue = None
    fields: list[ErrorField] = []
    try:
        envelope = ErrorResponse.model_validate(decoded)
    except PydanticValidationError:
        return code, message, request_id, response.text[:2048], fields

    code = envelope.code
    message = envelope.message
    request_id = envelope.request_id or request_id
    details = envelope.details
    fields = envelope.fields
    if details is None:
        extra = {
            key: value for key, value in decoded.items() if key not in _ERROR_FIELDS
        }
        if extra:
            details = cast(JSONValue, extra)
    return code, message, request_id, details, fields


def _api_error(response: httpx.Response, method: str) -> FrontalError:
    request_id = response.headers.get("x-request-id")
    code: str | None = None
    message = f"Frontal API request failed with HTTP {response.status_code}"
    details: JSONValue = None
    fields: list[ErrorField] = []
    decoded = _decode_error_body(response)
    if isinstance(decoded, dict) and _ERROR_FIELDS.intersection(decoded):
        code, message, request_id, details, fields = _error_envelope(
            decoded, response, request_id
        )
    elif response.content:
        details = decoded if isinstance(decoded, (dict, list)) else response.text[:2048]

    return error_for_status(
        response.status_code,
        message,
        code=code,
        request_id=request_id,
        details=details,
        fields=fields,
        retry_after=_parse_retry_after(response.headers.get("retry-after")),
        safe_to_retry=method in {"GET", "HEAD", "OPTIONS", "PUT", "DELETE"},
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
    ceiling = float(min(0.1 * (2**attempt), 2.0))
    return random.uniform(0.0, ceiling)


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
        # SSE's last-event-ID buffer persists until another non-empty id field.
        return "message", event_id, [], parsed_event
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


def _stream_retry_count(operation: Operation, max_retries: int | None) -> int:
    if operation.method != "POST":
        raise ValueError("stream_request() requires a POST operation")
    retries = 0 if max_retries is None else max_retries
    if isinstance(retries, bool) or not isinstance(retries, int):
        raise TypeError("max_retries must be an integer")
    if not 0 <= retries <= 10:
        raise ValueError("max_retries must be between 0 and 10")
    return retries


def _stream_response_retry_delay(
    response: httpx.Response, attempt: int, retries: int
) -> float | None:
    if response.status_code not in _RETRYABLE_STATUS or attempt >= retries:
        return None
    return _retry_delay(
        attempt, _parse_retry_after(response.headers.get("retry-after"))
    )


def _check_stream_response(response: httpx.Response) -> None:
    if response.is_error:
        raise _api_error(response, "POST")
    if response.headers.get("content-type", "").startswith(_EVENT_STREAM_CONTENT_TYPE):
        return
    raise FrontalError(
        _EVENT_STREAM_ERROR,
        request_id=response.headers.get("x-request-id"),
        status_code=response.status_code,
    )


def _stream_events(response: httpx.Response) -> Iterator[ServerEvent]:
    _check_stream_response(response)
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


async def _async_stream_events(response: httpx.Response) -> AsyncIterator[ServerEvent]:
    _check_stream_response(response)
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


def _can_retry_stream_error(
    error: FrontalError | httpx.RequestError | httpx.TimeoutException,
    emitted: bool,
    attempt: int,
    retries: int,
) -> bool:
    if emitted or attempt >= retries:
        return False
    if isinstance(error, FrontalError):
        return error.transient
    return True


def _raise_stream_error(
    error: FrontalError | httpx.RequestError | httpx.TimeoutException,
) -> None:
    if isinstance(error, FrontalError):
        raise error
    if isinstance(error, httpx.TimeoutException):
        raise TimeoutError(f"Stream request timed out: {error}") from error
    raise NetworkError(f"Stream request failed: {error}") from error


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
        body: RequestBodyInput = UNSET,
    ) -> JSONValue:
        """Call one catalogued operation and validate the JSON response."""
        if operation.method in {"GETRAW", "STREAM", "POSTFORMDATA", "POSTRAW"}:
            raise ValueError(
                "use request_bytes(), stream(), request_multipart(), or request_raw()"
            )
        url = _request_url(self._config.base_url, operation, path_params, query)
        content = _request_body_bytes(body)
        headers = _headers(
            self._config,
            {"Content-Type": "application/json"} if content is not None else None,
        )
        request = self._client.build_request(
            operation.method,
            url,
            headers=headers,
            content=content,
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
        emitted = False
        while True:
            try:
                with self._client.stream(
                    "GET",
                    url,
                    headers=_headers(
                        self._config, {"Accept": _EVENT_STREAM_CONTENT_TYPE}
                    ),
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
                        raise _api_error(response, "GET")
                    if not response.headers.get("content-type", "").startswith(
                        _EVENT_STREAM_CONTENT_TYPE
                    ):
                        raise FrontalError(
                            _EVENT_STREAM_ERROR,
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
                            emitted = True
                            yield parsed
                    if data_lines:
                        emitted = True
                        yield _event(event, event_id, data_lines)
                    return
            except httpx.TimeoutException as error:
                if not emitted and attempt < self._config.max_retries:
                    time_sleep(_retry_delay(attempt, None))
                    attempt += 1
                    continue
                raise TimeoutError(
                    f"Stream request timed out: {error}", safe_to_retry=True
                ) from error
            except httpx.RequestError as error:
                if not emitted and attempt < self._config.max_retries:
                    time_sleep(_retry_delay(attempt, None))
                    attempt += 1
                    continue
                raise NetworkError(
                    f"Stream request failed: {error}", safe_to_retry=True
                ) from error

    def stream_request(
        self,
        operation: Operation,
        *,
        body: RequestBody,
        max_retries: int | None = None,
    ) -> Iterator[ServerEvent]:
        """Send a JSON POST and yield SSE events.

        Retries default to zero because a failed connection may follow server
        acceptance. Set ``max_retries`` only when replaying is safe.
        """
        retries = _stream_retry_count(operation, max_retries)
        content = _json_body_bytes(body)
        url = _request_url(self._config.base_url, operation, (), None)
        attempt = 0
        emitted = False
        while True:
            try:
                with self._client.stream(
                    "POST",
                    url,
                    headers=_headers(
                        self._config,
                        {
                            "Accept": _EVENT_STREAM_CONTENT_TYPE,
                            "Content-Type": "application/json",
                        },
                    ),
                    content=content,
                ) as response:
                    delay = _stream_response_retry_delay(response, attempt, retries)
                    if delay is not None:
                        time_sleep(delay)
                        attempt += 1
                        continue
                    for event in _stream_events(response):
                        emitted = True
                        yield event
                    return
            except (FrontalError, httpx.TimeoutException, httpx.RequestError) as error:
                if _can_retry_stream_error(error, emitted, attempt, retries):
                    time_sleep(_retry_delay(attempt, None))
                    attempt += 1
                    continue
                _raise_stream_error(error)

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
                    _LOGGER.debug(
                        "Frontal request %s %s", request.method, request.url.path
                    )
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
                    raise _api_error(response, method)
                return response
            except httpx.TimeoutException as error:
                if method == "GET" and attempt < self._config.max_retries:
                    time_sleep(_retry_delay(attempt, None))
                    attempt += 1
                    continue
                raise TimeoutError(
                    f"Request timed out: {error}",
                    safe_to_retry=method in {"GET", "HEAD", "OPTIONS", "PUT", "DELETE"},
                ) from error
            except httpx.RequestError as error:
                if method == "GET" and attempt < self._config.max_retries:
                    time_sleep(_retry_delay(attempt, None))
                    attempt += 1
                    continue
                raise NetworkError(
                    f"Request failed: {error}",
                    safe_to_retry=method in {"GET", "HEAD", "OPTIONS", "PUT", "DELETE"},
                ) from error


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
        body: RequestBodyInput = UNSET,
    ) -> Coroutine[Any, Any, JSONValue]:
        """Call one catalogued operation and validate the JSON response."""
        return self._request(operation, path_params=path_params, query=query, body=body)

    async def _request(
        self,
        operation: Operation,
        *,
        path_params: Sequence[str],
        query: QueryParams | None,
        body: RequestBodyInput,
    ) -> JSONValue:
        if operation.method in {"GETRAW", "STREAM", "POSTFORMDATA", "POSTRAW"}:
            raise ValueError(
                "use request_bytes(), stream(), request_multipart(), or request_raw()"
            )
        content = _request_body_bytes(body)
        headers = _headers(
            self._config,
            {"Content-Type": "application/json"} if content is not None else None,
        )
        request = self._client.build_request(
            operation.method,
            _request_url(self._config.base_url, operation, path_params, query),
            headers=headers,
            content=content,
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
        emitted = False
        while True:
            try:
                async with self._client.stream(
                    "GET",
                    url,
                    headers=_headers(
                        self._config, {"Accept": _EVENT_STREAM_CONTENT_TYPE}
                    ),
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
                        raise _api_error(response, "GET")
                    if not response.headers.get("content-type", "").startswith(
                        _EVENT_STREAM_CONTENT_TYPE
                    ):
                        raise FrontalError(
                            _EVENT_STREAM_ERROR,
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
                            emitted = True
                            yield parsed
                    if data_lines:
                        emitted = True
                        yield _event(event, event_id, data_lines)
                    return
            except httpx.TimeoutException as error:
                if not emitted and attempt < self._config.max_retries:
                    await anyio.sleep(_retry_delay(attempt, None))
                    attempt += 1
                    continue
                raise TimeoutError(
                    f"Stream request timed out: {error}", safe_to_retry=True
                ) from error
            except httpx.RequestError as error:
                if not emitted and attempt < self._config.max_retries:
                    await anyio.sleep(_retry_delay(attempt, None))
                    attempt += 1
                    continue
                raise NetworkError(
                    f"Stream request failed: {error}", safe_to_retry=True
                ) from error

    async def stream_request(
        self,
        operation: Operation,
        *,
        body: RequestBody,
        max_retries: int | None = None,
    ) -> AsyncIterator[ServerEvent]:
        """Send a JSON POST and asynchronously yield SSE events.

        Retries default to zero because a failed connection may follow server
        acceptance. Set ``max_retries`` only when replaying is safe.
        """
        retries = _stream_retry_count(operation, max_retries)
        content = _json_body_bytes(body)
        url = _request_url(self._config.base_url, operation, (), None)
        attempt = 0
        emitted = False
        while True:
            try:
                async with self._client.stream(
                    "POST",
                    url,
                    headers=_headers(
                        self._config,
                        {
                            "Accept": _EVENT_STREAM_CONTENT_TYPE,
                            "Content-Type": "application/json",
                        },
                    ),
                    content=content,
                ) as response:
                    delay = _stream_response_retry_delay(response, attempt, retries)
                    if delay is not None:
                        await anyio.sleep(delay)
                        attempt += 1
                        continue
                    async for event in _async_stream_events(response):
                        emitted = True
                        yield event
                    return
            except (FrontalError, httpx.TimeoutException, httpx.RequestError) as error:
                if _can_retry_stream_error(error, emitted, attempt, retries):
                    await anyio.sleep(_retry_delay(attempt, None))
                    attempt += 1
                    continue
                _raise_stream_error(error)

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
                    _LOGGER.debug(
                        "Frontal request %s %s", request.method, request.url.path
                    )
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
                    raise _api_error(response, method)
                return response
            except httpx.TimeoutException as error:
                if method == "GET" and attempt < self._config.max_retries:
                    await anyio.sleep(_retry_delay(attempt, None))
                    attempt += 1
                    continue
                raise TimeoutError(
                    f"Request timed out: {error}",
                    safe_to_retry=method in {"GET", "HEAD", "OPTIONS", "PUT", "DELETE"},
                ) from error
            except httpx.RequestError as error:
                if method == "GET" and attempt < self._config.max_retries:
                    await anyio.sleep(_retry_delay(attempt, None))
                    attempt += 1
                    continue
                raise NetworkError(
                    f"Request failed: {error}",
                    safe_to_retry=method in {"GET", "HEAD", "OPTIONS", "PUT", "DELETE"},
                ) from error


__all__ = ["AsyncHttpClient", "HttpClient"]

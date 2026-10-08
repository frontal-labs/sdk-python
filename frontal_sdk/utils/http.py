"""Synchronous HTTP transport with authentication, retries, and typed errors."""

from __future__ import annotations

import json
import time
import uuid
from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass
from email.message import Message
from typing import cast
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen

from frontal_sdk.api_types import JSONValue
from frontal_sdk.utils.config import ClientConfig
from frontal_sdk.utils.errors import FrontalError
from frontal_sdk.utils.operation import Operation

_RETRYABLE_STATUS = {429, 500, 502, 503, 504}


@dataclass(frozen=True, slots=True)
class MultipartPart:
    """One file field in a multipart request."""

    name: str
    data: bytes
    filename: str
    content_type: str = "application/octet-stream"


@dataclass(frozen=True, slots=True)
class ServerEvent:
    """Parsed server-sent event frame."""

    event: str
    data: JSONValue
    id: str | None


class HttpClient:
    """Owns the HTTP configuration used by every service on a client."""

    def __init__(self, config: ClientConfig) -> None:
        self._config = config

    def request(
        self,
        operation: Operation,
        *,
        path_params: Sequence[str] = (),
        query: Mapping[str, str | int | float | bool] | None = None,
        body: JSONValue = None,
    ) -> JSONValue:
        """Call one catalogued operation and decode its JSON response."""
        if operation.method in {"GETRAW", "STREAM", "POSTFORMDATA", "POSTRAW"}:
            raise ValueError(
                "use request_bytes(), stream(), request_multipart(), or request_raw()"
            )
        path = operation.render_path(tuple(path_params))
        url = self._build_url(path, query)
        request_body = None if body is None else json.dumps(body).encode("utf-8")
        extra_headers = (
            {"Content-Type": "application/json"} if request_body is not None else {}
        )
        request = Request(
            url,
            data=request_body,
            headers=self._headers(extra_headers),
            method=operation.method,
        )

        payload, response_headers = self._send(request, operation.method)
        return self._decode(payload, response_headers)

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
        boundary = f"frontal-{uuid.uuid4().hex}"
        chunks: list[bytes] = []
        for name, value in (fields or {}).items():
            chunks.extend(
                [
                    f"--{boundary}\r\n".encode(),
                    f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode(),
                    value.encode("utf-8"),
                    b"\r\n",
                ]
            )
        for part in parts:
            chunks.extend(
                [
                    f"--{boundary}\r\n".encode(),
                    (
                        f'Content-Disposition: form-data; name="{part.name}"; '
                        f'filename="{part.filename}"\r\n'
                    ).encode(),
                    f"Content-Type: {part.content_type}\r\n\r\n".encode(),
                    part.data,
                    b"\r\n",
                ]
            )
        chunks.append(f"--{boundary}--\r\n".encode())
        request = Request(
            self._build_url(operation.render_path(tuple(path_params)), None),
            data=b"".join(chunks),
            headers=self._headers(
                {"Content-Type": f"multipart/form-data; boundary={boundary}"}
            ),
            method="POST",
        )
        payload, response_headers = self._send(request, "POST")
        return self._decode(payload, response_headers)

    def request_raw(
        self,
        operation: Operation,
        data: bytes,
        content_type: str,
        *,
        path_params: Sequence[str] = (),
        query: Mapping[str, str | int | float | bool] | None = None,
    ) -> bytes:
        """Send raw bytes to a POSTRAW operation and return response bytes."""
        if operation.method != "POSTRAW":
            raise ValueError("request_raw() requires POSTRAW")
        request = Request(
            self._build_url(operation.render_path(tuple(path_params)), query),
            data=data,
            headers=self._headers({"Content-Type": content_type}),
            method="POST",
        )
        payload, _ = self._send(request, "POST")
        return payload

    def request_bytes(
        self,
        operation: Operation,
        *,
        path_params: Sequence[str] = (),
        query: Mapping[str, str | int | float | bool] | None = None,
    ) -> bytes:
        """Read a successful non-streaming response without JSON decoding."""
        if operation.method in {"STREAM", "POSTFORMDATA", "POSTRAW"}:
            raise ValueError("use stream(), request_multipart(), or request_raw()")
        request = Request(
            self._build_url(operation.render_path(tuple(path_params)), query),
            headers=self._headers({"Accept": "*/*"}),
            method="GET" if operation.method == "GETRAW" else operation.method,
        )
        payload, _ = self._send(
            request, "GET" if operation.method == "GETRAW" else operation.method
        )
        return payload

    def stream(
        self,
        operation: Operation,
        *,
        path_params: Sequence[str] = (),
        query: Mapping[str, str | int | float | bool] | None = None,
    ) -> Iterator[ServerEvent]:
        """Yield parsed SSE frames; closing the iterator releases the socket."""
        if operation.method != "STREAM":
            raise ValueError("stream() requires a STREAM operation")
        request = Request(
            self._build_url(operation.render_path(tuple(path_params)), query),
            headers=self._headers({"Accept": "text/event-stream"}),
            method="GET",
        )
        try:
            with urlopen(request, timeout=self._config.timeout) as response:
                if not response.headers.get_content_type().startswith(
                    "text/event-stream"
                ):
                    raise FrontalError("The API did not return an event stream")
                event = "message"
                event_id: str | None = None
                data_lines: list[str] = []
                for raw_line in response:
                    line = raw_line.decode("utf-8").rstrip("\r\n")
                    if line == "":
                        if data_lines:
                            yield self._event(event, event_id, data_lines)
                        event, event_id, data_lines = "message", None, []
                    elif line.startswith(":"):
                        continue
                    elif ":" in line:
                        field, value = line.split(":", 1)
                        value = value.removeprefix(" ")
                        if field == "event":
                            event = value or "message"
                        elif field == "id" and "\0" not in value:
                            event_id = value
                        elif field == "data":
                            data_lines.append(value)
                if data_lines:
                    yield self._event(event, event_id, data_lines)
        except HTTPError as error:
            raise self._api_error(error.code, error.read(), error.headers) from error
        except (URLError, TimeoutError, OSError) as error:
            raise FrontalError(f"Stream request failed: {error}") from error

    @staticmethod
    def _event(event: str, event_id: str | None, lines: list[str]) -> ServerEvent:
        payload = "\n".join(lines)
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            data = payload
        return ServerEvent(event, data, event_id)

    def _headers(self, extra: Mapping[str, str] | None = None) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._config.api_key}",
            "Accept": "application/json",
            "User-Agent": "frontal-sdk-python/0.1.0",
            **self._config.headers,
            **(extra or {}),
        }

    def _send(self, request: Request, method: str) -> tuple[bytes, Message]:
        attempt = 0
        while True:
            try:
                with urlopen(request, timeout=self._config.timeout) as response:
                    return response.read(), response.headers
            except HTTPError as error:
                payload = error.read()
                if (
                    method == "GET"
                    and error.code in _RETRYABLE_STATUS
                    and attempt < self._config.max_retries
                ):
                    time.sleep(self._retry_delay(attempt, error.headers))
                    attempt += 1
                    continue
                raise self._api_error(error.code, payload, error.headers) from error
            except (URLError, TimeoutError, OSError) as error:
                raise FrontalError(f"Request failed: {error}") from error

    def _build_url(
        self,
        path: str,
        query: Mapping[str, str | int | float | bool] | None,
    ) -> str:
        fixed = urlsplit(path)
        base = urlsplit(self._config.base_url)
        combined_query = parse_qsl(fixed.query, keep_blank_values=True)
        if query:
            combined_query.extend((key, str(value)) for key, value in query.items())
        return urlunsplit(
            (
                base.scheme,
                base.netloc,
                f"{base.path.rstrip('/')}{fixed.path}",
                urlencode(combined_query),
                "",
            )
        )

    @staticmethod
    def _decode(payload: bytes, headers: Message) -> JSONValue:
        if not payload:
            return None
        content_type = headers.get_content_type()
        if content_type != "application/json" and not content_type.endswith("+json"):
            raise FrontalError(f"Expected JSON response, received {content_type}")
        try:
            return cast(JSONValue, json.loads(payload))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise FrontalError("The API returned invalid JSON") from error

    @classmethod
    def _api_error(
        cls,
        status: int,
        payload: bytes,
        headers: Message,
    ) -> FrontalError:
        request_id = headers.get("x-request-id")
        code: str | None = None
        message = f"Frontal API request failed with HTTP {status}"
        details: JSONValue = None
        try:
            decoded = json.loads(payload) if payload else None
            if isinstance(decoded, dict):
                code_value = decoded.get("code")
                message_value = decoded.get("message")
                request_id_value = decoded.get("requestId", decoded.get("request_id"))
                code = code_value if isinstance(code_value, str) else None
                message = message_value if isinstance(message_value, str) else message
                request_id = (
                    request_id_value
                    if isinstance(request_id_value, str)
                    else request_id
                )
                details = cast(JSONValue, decoded.get("details"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            details = payload.decode("utf-8", errors="replace")
        return FrontalError(
            message,
            status_code=status,
            code=code,
            request_id=request_id,
            details=details,
        )

    @staticmethod
    def _retry_delay(attempt: int, headers: Message) -> float:
        retry_after = headers.get("Retry-After")
        if retry_after is not None:
            try:
                return min(max(float(retry_after), 0.0), 5.0)
            except ValueError:
                pass
        return float(min(0.1 * (2**attempt), 2.0))

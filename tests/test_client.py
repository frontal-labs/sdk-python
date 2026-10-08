"""Transport integration tests against a local HTTP server."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from typing import cast
from urllib.parse import urlsplit

import pytest
from frontal_sdk import Frontal, FrontalError
from frontal_sdk.services.agents import AgentsEndpoint
from frontal_sdk.services.auth import AuthEndpoint
from frontal_sdk.services.blob import BlobEndpoint
from frontal_sdk.utils import ClientConfig, HttpClient, MultipartPart
from frontal_sdk.utils.operation import Operation


class ApiHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    requests_seen: list[dict[str, object]] = []
    retry_calls = 0

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/v1/agents" and type(self).retry_calls == 0:
            type(self).retry_calls += 1
            self.send_response(503)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        self._record()
        if self.path == "/v1/failure":
            self._write(401, {"code": "UNAUTHORIZED", "message": "denied"})
        elif self.headers.get("Accept") == "text/event-stream":
            payload = b'event: state\nid: evt_1\ndata: {"ready":true}\n\n'
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        else:
            self._write(200, self.requests_seen[-1])

    def do_POST(self) -> None:  # noqa: N802
        self._record()
        self._write(201, self.requests_seen[-1])

    def _record(self) -> None:
        body = self.rfile.read(int(self.headers.get("Content-Length", "0")))
        try:
            decoded: object = json.loads(body) if body else None
        except json.JSONDecodeError:
            decoded = body.decode("utf-8", errors="replace")
        type(self).requests_seen.append(
            {
                "method": self.command,
                "path": self.path,
                "authorization": self.headers.get("Authorization"),
                "content_type": self.headers.get("Content-Type"),
                "body": decoded,
            }
        )

    def _write(self, status: int, payload: object) -> None:
        encoded = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("X-Request-Id", "req_local_1")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, format: str, *args: object) -> None:
        return


@pytest.fixture
def api_server() -> tuple[str, ThreadingHTTPServer]:
    ApiHandler.requests_seen = []
    ApiHandler.retry_calls = 0
    server = ThreadingHTTPServer(("127.0.0.1", 0), ApiHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    yield f"http://{host}:{port}/v1", server
    server.shutdown()
    thread.join(timeout=2)
    server.server_close()


def test_service_calls_use_auth_query_and_encoded_path(
    api_server: tuple[str, ThreadingHTTPServer],
) -> None:
    base_url, _server = api_server
    client = Frontal("frt_local_key", base_url=base_url, max_retries=1)

    response = client.agents.call(
        AgentsEndpoint.GET_AGENTS_PARAM_1,
        path_params=("agent/one",),
        query={"include_runs": True},
    )

    payload = cast(dict[str, object], response)
    assert payload["path"] == "/v1/agents/agent%2Fone?include_runs=True"
    assert payload["authorization"] == "Bearer frt_local_key"
    client_text = urlsplit(base_url).path
    assert client_text == "/v1"


def test_post_serializes_json_and_uses_catalogued_operation(
    api_server: tuple[str, ThreadingHTTPServer],
) -> None:
    base_url, _server = api_server
    client = Frontal("frt_local_key", base_url=base_url)

    result = client.auth.call(
        AuthEndpoint.POST_AUTH_SIGNUP,
        body={"email": "person@example.com", "metadata": {"source": "test"}},
    )

    payload = cast(dict[str, object], result)
    assert payload["method"] == "POST"
    assert payload["body"] == {
        "email": "person@example.com",
        "metadata": {"source": "test"},
    }
    assert payload["content_type"] == "application/json"


def test_get_retries_transient_server_errors(
    api_server: tuple[str, ThreadingHTTPServer],
) -> None:
    base_url, _server = api_server
    client = Frontal("frt_local_key", base_url=base_url, max_retries=1)

    result = client.agents.call(AgentsEndpoint.GET_AGENTS)

    assert cast(dict[str, object], result)["path"] == "/v1/agents"
    assert ApiHandler.retry_calls == 1


def test_structured_api_error(api_server: tuple[str, ThreadingHTTPServer]) -> None:
    base_url, _server = api_server
    client = HttpClient(ClientConfig("frt_local_key", base_url=base_url))

    with pytest.raises(FrontalError) as raised:
        client.request(Operation("GET", "/failure"))

    assert raised.value.status_code == 401
    assert raised.value.code == "UNAUTHORIZED"
    assert raised.value.request_id == "req_local_1"


def test_multipart_upload_and_raw_binary_response(
    api_server: tuple[str, ThreadingHTTPServer],
) -> None:
    base_url, _server = api_server
    client = Frontal("frt_local_key", base_url=base_url)

    upload = client.blob.upload(
        BlobEndpoint.POST_FORM_DATA_BLOB_OBJECT_PARAM_1_PARAM_2,
        [
            MultipartPart(
                "file",
                b"file-content",
                filename="report.txt",
                content_type="text/plain",
            )
        ],
        path_params=("reports", "report.txt"),
        fields={"cacheControl": "3600"},
    )
    downloaded = client.blob.request_bytes(
        BlobEndpoint.GET_BLOB_OBJECT_PARAM_1_PARAM_2,
        path_params=("reports", "report.txt"),
    )

    assert cast(dict[str, object], upload)["method"] == "POST"
    assert downloaded.startswith(b"{")
    assert any(
        "multipart/form-data" in str(request["content_type"])
        for request in ApiHandler.requests_seen
    )


def test_sse_stream_is_parsed(api_server: tuple[str, ThreadingHTTPServer]) -> None:
    base_url, _server = api_server
    client = Frontal("frt_local_key", base_url=base_url)

    events = list(
        client.agents.stream(
            AgentsEndpoint.STREAM_AGENTS_RUNS_PARAM_1_STREAM,
            path_params=("run_1",),
        )
    )

    assert [(event.event, event.id, event.data) for event in events] == [
        ("state", "evt_1", {"ready": True})
    ]

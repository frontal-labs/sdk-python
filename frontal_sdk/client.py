"""Unified synchronous and asynchronous clients for the Frontal API."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator, Coroutine, Iterator, Mapping
from typing import Any

import httpx

from frontal_sdk.core.config import ClientConfig
from frontal_sdk.core.http import AsyncHttpClient, HttpClient
from frontal_sdk.models import JSONValue, ServerEvent
from frontal_sdk.resources import (
    Agents,
    AsyncAI,
    Audit,
    Auth,
    Billing,
    Blob,
    Connectors,
    Data,
    Governance,
    Lineage,
    Observability,
    Ontology,
    Pipelines,
    Sandbox,
    Schedules,
    SyncAI,
    Webhooks,
    Workflows,
)

_DEFAULT_BASE_URL = "https://api.frontal.dev/v1"
_AsyncJSONResult = Coroutine[Any, Any, JSONValue]
_AsyncBytesResult = Coroutine[Any, Any, bytes]
_AsyncStreamResult = AsyncIterator[ServerEvent]


def _environment_bool(value: str | None) -> bool:
    return value is not None and value.strip().lower() in {"1", "true", "yes", "on"}


def _config(
    api_key: str | None,
    base_url: str | None,
    timeout: float,
    max_retries: int,
    headers: Mapping[str, str] | None,
    environment: str | None,
    debug: bool | None,
) -> ClientConfig:
    key = api_key if api_key is not None else os.environ.get("FRONTAL_API_KEY")
    if not key:
        raise ValueError("api_key is required; pass it or set FRONTAL_API_KEY")
    return ClientConfig(
        api_key=key,
        base_url=(
            base_url
            if base_url is not None
            else os.environ.get("FRONTAL_API_URL", _DEFAULT_BASE_URL)
        ),
        timeout=timeout,
        max_retries=max_retries,
        headers=headers or {},
        environment=(
            environment
            if environment is not None
            else os.environ.get("FRONTAL_ENV", "production")
        ),
        debug=(
            debug
            if debug is not None
            else _environment_bool(os.environ.get("FRONTAL_DEBUG"))
        ),
    )


class Frontal:
    """Synchronous API client with typed service namespaces.

    ``api_key`` defaults to ``FRONTAL_API_KEY``. The base URL, environment,
    and debug setting also read ``FRONTAL_API_URL``, ``FRONTAL_ENV``, and
    ``FRONTAL_DEBUG`` when their matching arguments are omitted. A supplied
    ``http_client`` remains caller-owned and keeps its own timeout configuration.
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        headers: Mapping[str, str] | None = None,
        environment: str | None = None,
        debug: bool | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        config = _config(
            api_key, base_url, timeout, max_retries, headers, environment, debug
        )
        http = HttpClient(config, http_client)
        self._http = http
        self.agents: Agents[JSONValue, bytes, Iterator[ServerEvent]] = Agents(http)
        self.ai: SyncAI = SyncAI(http)
        self.audit: Audit[JSONValue, bytes, Iterator[ServerEvent]] = Audit(http)
        self.auth: Auth[JSONValue, bytes, Iterator[ServerEvent]] = Auth(http)
        self.billing: Billing[JSONValue, bytes, Iterator[ServerEvent]] = Billing(http)
        self.blob: Blob[JSONValue, bytes, Iterator[ServerEvent]] = Blob(http)
        self.connectors: Connectors[JSONValue, bytes, Iterator[ServerEvent]] = (
            Connectors(http)
        )
        self.data: Data[JSONValue, bytes, Iterator[ServerEvent]] = Data(http)
        self.governance: Governance[JSONValue, bytes, Iterator[ServerEvent]] = (
            Governance(http)
        )
        self.lineage: Lineage[JSONValue, bytes, Iterator[ServerEvent]] = Lineage(http)
        self.observability: Observability[JSONValue, bytes, Iterator[ServerEvent]] = (
            Observability(http)
        )
        self.ontology: Ontology[JSONValue, bytes, Iterator[ServerEvent]] = Ontology(
            http
        )
        self.pipelines: Pipelines[JSONValue, bytes, Iterator[ServerEvent]] = Pipelines(
            http
        )
        self.sandbox: Sandbox[JSONValue, bytes, Iterator[ServerEvent]] = Sandbox(http)
        self.schedules: Schedules[JSONValue, bytes, Iterator[ServerEvent]] = Schedules(
            http
        )
        self.webhooks: Webhooks[JSONValue, bytes, Iterator[ServerEvent]] = Webhooks(
            http
        )
        self.workflows: Workflows[JSONValue, bytes, Iterator[ServerEvent]] = Workflows(
            http
        )

    @classmethod
    def from_env(cls) -> Frontal:
        """Create a client from the ``FRONTAL_*`` environment variables."""
        return cls()

    def close(self) -> None:
        """Close this client's HTTP connection pool."""
        self._http.close()

    def __enter__(self) -> Frontal:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


class AsyncFrontal:
    """Async client with matching typed services.

    A supplied ``http_client`` remains caller-owned and keeps its own timeout
    configuration.
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        headers: Mapping[str, str] | None = None,
        environment: str | None = None,
        debug: bool | None = None,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        config = _config(
            api_key, base_url, timeout, max_retries, headers, environment, debug
        )
        http = AsyncHttpClient(config, http_client)
        self._http = http
        self.agents: Agents[_AsyncJSONResult, _AsyncBytesResult, _AsyncStreamResult] = (
            Agents(http)
        )
        self.ai: AsyncAI = AsyncAI(http)
        self.audit: Audit[_AsyncJSONResult, _AsyncBytesResult, _AsyncStreamResult] = (
            Audit(http)
        )
        self.auth: Auth[_AsyncJSONResult, _AsyncBytesResult, _AsyncStreamResult] = Auth(
            http
        )
        self.billing: Billing[
            _AsyncJSONResult, _AsyncBytesResult, _AsyncStreamResult
        ] = Billing(http)
        self.blob: Blob[_AsyncJSONResult, _AsyncBytesResult, _AsyncStreamResult] = Blob(
            http
        )
        self.connectors: Connectors[
            _AsyncJSONResult, _AsyncBytesResult, _AsyncStreamResult
        ] = Connectors(http)
        self.data: Data[_AsyncJSONResult, _AsyncBytesResult, _AsyncStreamResult] = Data(
            http
        )
        self.governance: Governance[
            _AsyncJSONResult, _AsyncBytesResult, _AsyncStreamResult
        ] = Governance(http)
        self.lineage: Lineage[
            _AsyncJSONResult, _AsyncBytesResult, _AsyncStreamResult
        ] = Lineage(http)
        self.observability: Observability[
            _AsyncJSONResult, _AsyncBytesResult, _AsyncStreamResult
        ] = Observability(http)
        self.ontology: Ontology[
            _AsyncJSONResult, _AsyncBytesResult, _AsyncStreamResult
        ] = Ontology(http)
        self.pipelines: Pipelines[
            _AsyncJSONResult, _AsyncBytesResult, _AsyncStreamResult
        ] = Pipelines(http)
        self.sandbox: Sandbox[
            _AsyncJSONResult, _AsyncBytesResult, _AsyncStreamResult
        ] = Sandbox(http)
        self.schedules: Schedules[
            _AsyncJSONResult, _AsyncBytesResult, _AsyncStreamResult
        ] = Schedules(http)
        self.webhooks: Webhooks[
            _AsyncJSONResult, _AsyncBytesResult, _AsyncStreamResult
        ] = Webhooks(http)
        self.workflows: Workflows[
            _AsyncJSONResult, _AsyncBytesResult, _AsyncStreamResult
        ] = Workflows(http)

    @classmethod
    def from_env(cls) -> AsyncFrontal:
        """Create an async client from the ``FRONTAL_*`` environment variables."""
        return cls()

    async def aclose(self) -> None:
        """Close this client's HTTP connection pool."""
        await self._http.aclose()

    async def __aenter__(self) -> AsyncFrontal:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.aclose()

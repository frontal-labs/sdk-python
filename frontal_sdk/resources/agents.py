"""Typed API resource for the agents endpoints."""

from __future__ import annotations

from typing import Generic

from frontal_sdk.core.operation import Operation
from frontal_sdk.models import QueryParams, RequestBody
from frontal_sdk.resources._base import (
    APIResource,
    BytesResultT,
    JSONResultT,
    StreamResultT,
)


class Agents(
    APIResource[JSONResultT, BytesResultT, StreamResultT],
    Generic[JSONResultT, BytesResultT, StreamResultT],
):
    """Methods for the agents API endpoints."""

    def delete_agents_by_param_1(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /agents/{param}."""
        return self._request(
            Operation("DELETE", "/agents/{param}"),
            path_params=(param_1,),
            query=query,
        )

    def get_agents(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /agents."""
        return self._request(
            Operation("GET", "/agents"),
            path_params=(),
            query=query,
        )

    def get_agents_by_param_1(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /agents/{param}."""
        return self._request(
            Operation("GET", "/agents/{param}"),
            path_params=(param_1,),
            query=query,
        )

    def get_agents_by_param_1_runs(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /agents/{param}/runs."""
        return self._request(
            Operation("GET", "/agents/{param}/runs"),
            path_params=(param_1,),
            query=query,
        )

    def get_agents_by_param_1_versions(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /agents/{param}/versions."""
        return self._request(
            Operation("GET", "/agents/{param}/versions"),
            path_params=(param_1,),
            query=query,
        )

    def get_agents_health(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /agents/health."""
        return self._request(
            Operation("GET", "/agents/health"),
            path_params=(),
            query=query,
        )

    def get_agents_runs_by_param_1(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /agents/runs/{param}."""
        return self._request(
            Operation("GET", "/agents/runs/{param}"),
            path_params=(param_1,),
            query=query,
        )

    def get_agents_runs_by_param_1_conversation(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /agents/runs/{param}/conversation."""
        return self._request(
            Operation("GET", "/agents/runs/{param}/conversation"),
            path_params=(param_1,),
            query=query,
        )

    def post_agents(
        self, *, query: QueryParams | None = None, body: RequestBody = None
    ) -> JSONResultT:
        """Call POST /agents."""
        return self._request(
            Operation("POST", "/agents"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_agents_by_param_1_rollback(
        self,
        param_1: str,
        *,
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONResultT:
        """Call POST /agents/{param}/rollback."""
        return self._request(
            Operation("POST", "/agents/{param}/rollback"),
            path_params=(param_1,),
            query=query,
            body=body,
        )

    def post_agents_by_param_1_runs(
        self,
        param_1: str,
        *,
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONResultT:
        """Call POST /agents/{param}/runs."""
        return self._request(
            Operation("POST", "/agents/{param}/runs"),
            path_params=(param_1,),
            query=query,
            body=body,
        )

    def put_agents_by_param_1(
        self,
        param_1: str,
        *,
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONResultT:
        """Call PUT /agents/{param}."""
        return self._request(
            Operation("PUT", "/agents/{param}"),
            path_params=(param_1,),
            query=query,
            body=body,
        )

    def stream_agents_runs_by_param_1_stream(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> StreamResultT:
        """Call STREAM /agents/runs/{param}/stream."""
        return self._stream(
            Operation("STREAM", "/agents/runs/{param}/stream"),
            path_params=(param_1,),
            query=query,
        )

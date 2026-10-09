"""Typed API resource for the pipelines endpoints."""

from __future__ import annotations

from typing import Generic

from frontal_sdk.core.operation import Operation
from frontal_sdk.models import QueryParams
from frontal_sdk.models.requests import UNSET, RequestBodyInput
from frontal_sdk.resources._base import (
    APIResource,
    BytesResultT,
    JSONResultT,
    StreamResultT,
)


class Pipelines(
    APIResource[JSONResultT, BytesResultT, StreamResultT],
    Generic[JSONResultT, BytesResultT, StreamResultT],
):
    """Methods for the pipelines API endpoints."""

    def list_capabilities(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /data/pipelines/capabilities."""
        return self._request(
            Operation("GET", "/data/pipelines/capabilities"),
            path_params=(),
            query=query,
        )

    def get_data_pipelines_health(
        self, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /data/pipelines/health."""
        return self._request(
            Operation("GET", "/data/pipelines/health"),
            path_params=(),
            query=query,
        )

    def get_data_pipelines_info(
        self, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /data/pipelines/info."""
        return self._request(
            Operation("GET", "/data/pipelines/info"),
            path_params=(),
            query=query,
        )

    def list_pipeline_runs(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /data/pipelines/pipeline-runs."""
        return self._request(
            Operation("GET", "/data/pipelines/pipeline-runs"),
            path_params=(),
            query=query,
        )

    def get_run(self, run_id: str, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /data/pipelines/pipeline-runs/{param}."""
        return self._request(
            Operation("GET", "/data/pipelines/pipeline-runs/{param}"),
            path_params=(run_id,),
            query=query,
        )

    def list_pipelines(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /data/pipelines/pipelines."""
        return self._request(
            Operation("GET", "/data/pipelines/pipelines"),
            path_params=(),
            query=query,
        )

    def get_definition(
        self, definition_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /data/pipelines/pipelines/{param}."""
        return self._request(
            Operation("GET", "/data/pipelines/pipelines/{param}"),
            path_params=(definition_id,),
            query=query,
        )

    def list_runs(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /data/pipelines/runs."""
        return self._request(
            Operation("GET", "/data/pipelines/runs"),
            path_params=(),
            query=query,
        )

    def create_pipeline(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /data/pipelines/pipelines."""
        return self._request(
            Operation("POST", "/data/pipelines/pipelines"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_run(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /data/pipelines/runs."""
        return self._request(
            Operation("POST", "/data/pipelines/runs"),
            path_params=(),
            query=query,
            body=body,
        )

    def stream_data_pipelines_pipeline_runs_by_run_id(
        self, run_id: str, *, query: QueryParams | None = None
    ) -> StreamResultT:
        """Call STREAM /data/pipelines/pipeline-runs/{param}."""
        return self._stream(
            Operation("STREAM", "/data/pipelines/pipeline-runs/{param}"),
            path_params=(run_id,),
            query=query,
        )

"""Typed API resource for the lineage endpoints."""

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


class Lineage(
    APIResource[JSONResultT, BytesResultT, StreamResultT],
    Generic[JSONResultT, BytesResultT, StreamResultT],
):
    """Methods for the lineage API endpoints."""

    def get_lineage_edges(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /lineage/edges."""
        return self._request(
            Operation("GET", "/lineage/edges"),
            path_params=(),
            query=query,
        )

    def get_lineage_edges_by_param_1(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /lineage/edges/{param}."""
        return self._request(
            Operation("GET", "/lineage/edges/{param}"),
            path_params=(param_1,),
            query=query,
        )

    def get_lineage_graph(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /lineage/graph."""
        return self._request(
            Operation("GET", "/lineage/graph"),
            path_params=(),
            query=query,
        )

    def get_lineage_nodes(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /lineage/nodes."""
        return self._request(
            Operation("GET", "/lineage/nodes"),
            path_params=(),
            query=query,
        )

    def get_lineage_nodes_by_param_1(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /lineage/nodes/{param}."""
        return self._request(
            Operation("GET", "/lineage/nodes/{param}"),
            path_params=(param_1,),
            query=query,
        )

    def get_lineage_nodes_by_param_1_trace(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /lineage/nodes/{param}/trace."""
        return self._request(
            Operation("GET", "/lineage/nodes/{param}/trace"),
            path_params=(param_1,),
            query=query,
        )

    def post_lineage_impact(
        self, *, query: QueryParams | None = None, body: RequestBody = None
    ) -> JSONResultT:
        """Call POST /lineage/impact."""
        return self._request(
            Operation("POST", "/lineage/impact"),
            path_params=(),
            query=query,
            body=body,
        )

"""Typed API resource for the connectors endpoints."""

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


class Connectors(
    APIResource[JSONResultT, BytesResultT, StreamResultT],
    Generic[JSONResultT, BytesResultT, StreamResultT],
):
    """Methods for the connectors API endpoints."""

    def delete_connectors_installations_by_param_1(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /connectors/installations/{param}."""
        return self._request(
            Operation("DELETE", "/connectors/installations/{param}"),
            path_params=(param_1,),
            query=query,
        )

    def get_connectors_catalog(
        self, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /connectors/catalog."""
        return self._request(
            Operation("GET", "/connectors/catalog"),
            path_params=(),
            query=query,
        )

    def get_connectors_catalog_by_param_1(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /connectors/catalog/{param}."""
        return self._request(
            Operation("GET", "/connectors/catalog/{param}"),
            path_params=(param_1,),
            query=query,
        )

    def get_connectors_connection_tests_by_param_1(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /connectors/connection-tests/{param}."""
        return self._request(
            Operation("GET", "/connectors/connection-tests/{param}"),
            path_params=(param_1,),
            query=query,
        )

    def get_connectors_installations(
        self, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /connectors/installations."""
        return self._request(
            Operation("GET", "/connectors/installations"),
            path_params=(),
            query=query,
        )

    def get_connectors_installations_by_param_1(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /connectors/installations/{param}."""
        return self._request(
            Operation("GET", "/connectors/installations/{param}"),
            path_params=(param_1,),
            query=query,
        )

    def get_diagnostics(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /diagnostics."""
        return self._request(
            Operation("GET", "/diagnostics"),
            path_params=(),
            query=query,
        )

    def patch_connectors_installations_by_param_1(
        self,
        param_1: str,
        *,
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONResultT:
        """Call PATCH /connectors/installations/{param}."""
        return self._request(
            Operation("PATCH", "/connectors/installations/{param}"),
            path_params=(param_1,),
            query=query,
            body=body,
        )

    def post_connectors_installations(
        self, *, query: QueryParams | None = None, body: RequestBody = None
    ) -> JSONResultT:
        """Call POST /connectors/installations."""
        return self._request(
            Operation("POST", "/connectors/installations"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_connectors_installations_by_param_1_pause(
        self,
        param_1: str,
        *,
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONResultT:
        """Call POST /connectors/installations/{param}/pause."""
        return self._request(
            Operation("POST", "/connectors/installations/{param}/pause"),
            path_params=(param_1,),
            query=query,
            body=body,
        )

    def post_connectors_installations_by_param_1_resume(
        self,
        param_1: str,
        *,
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONResultT:
        """Call POST /connectors/installations/{param}/resume."""
        return self._request(
            Operation("POST", "/connectors/installations/{param}/resume"),
            path_params=(param_1,),
            query=query,
            body=body,
        )

    def post_connectors_sync_runs_by_param_1_replay(
        self,
        param_1: str,
        *,
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONResultT:
        """Call POST /connectors/sync-runs/{param}/replay."""
        return self._request(
            Operation("POST", "/connectors/sync-runs/{param}/replay"),
            path_params=(param_1,),
            query=query,
            body=body,
        )

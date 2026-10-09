"""Typed API resource for the connectors endpoints."""

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


class Connectors(
    APIResource[JSONResultT, BytesResultT, StreamResultT],
    Generic[JSONResultT, BytesResultT, StreamResultT],
):
    """Methods for the connectors API endpoints."""

    def delete_installation(
        self, installation_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /connectors/installations/{param}."""
        return self._request(
            Operation("DELETE", "/connectors/installations/{param}"),
            path_params=(installation_id,),
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

    def get_catalog(
        self, catalog_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /connectors/catalog/{param}."""
        return self._request(
            Operation("GET", "/connectors/catalog/{param}"),
            path_params=(catalog_id,),
            query=query,
        )

    def get_connection_test(
        self, connection_test_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /connectors/connection-tests/{param}."""
        return self._request(
            Operation("GET", "/connectors/connection-tests/{param}"),
            path_params=(connection_test_id,),
            query=query,
        )

    def list_installations(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /connectors/installations."""
        return self._request(
            Operation("GET", "/connectors/installations"),
            path_params=(),
            query=query,
        )

    def get_installation(
        self, installation_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /connectors/installations/{param}."""
        return self._request(
            Operation("GET", "/connectors/installations/{param}"),
            path_params=(installation_id,),
            query=query,
        )

    def list_diagnostics(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /diagnostics."""
        return self._request(
            Operation("GET", "/diagnostics"),
            path_params=(),
            query=query,
        )

    def update_installation(
        self,
        installation_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call PATCH /connectors/installations/{param}."""
        return self._request(
            Operation("PATCH", "/connectors/installations/{param}"),
            path_params=(installation_id,),
            query=query,
            body=body,
        )

    def create_installation(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /connectors/installations."""
        return self._request(
            Operation("POST", "/connectors/installations"),
            path_params=(),
            query=query,
            body=body,
        )

    def pause_installation(
        self,
        installation_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /connectors/installations/{param}/pause."""
        return self._request(
            Operation("POST", "/connectors/installations/{param}/pause"),
            path_params=(installation_id,),
            query=query,
            body=body,
        )

    def resume_installation(
        self,
        installation_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /connectors/installations/{param}/resume."""
        return self._request(
            Operation("POST", "/connectors/installations/{param}/resume"),
            path_params=(installation_id,),
            query=query,
            body=body,
        )

    def replay_sync_run(
        self,
        sync_run_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /connectors/sync-runs/{param}/replay."""
        return self._request(
            Operation("POST", "/connectors/sync-runs/{param}/replay"),
            path_params=(sync_run_id,),
            query=query,
            body=body,
        )

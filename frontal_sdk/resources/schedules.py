"""Typed API resource for the schedules endpoints."""

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


class Schedules(
    APIResource[JSONResultT, BytesResultT, StreamResultT],
    Generic[JSONResultT, BytesResultT, StreamResultT],
):
    """Methods for the schedules API endpoints."""

    def delete_schedule(
        self, schedule_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /workflows/schedules/{param}."""
        return self._request(
            Operation("DELETE", "/workflows/schedules/{param}"),
            path_params=(schedule_id,),
            query=query,
        )

    def list_schedules(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /workflows/schedules."""
        return self._request(
            Operation("GET", "/workflows/schedules"),
            path_params=(),
            query=query,
        )

    def get_schedule(
        self, schedule_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /workflows/schedules/{param}."""
        return self._request(
            Operation("GET", "/workflows/schedules/{param}"),
            path_params=(schedule_id,),
            query=query,
        )

    def update_schedule(
        self,
        schedule_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call PATCH /workflows/schedules/{param}."""
        return self._request(
            Operation("PATCH", "/workflows/schedules/{param}"),
            path_params=(schedule_id,),
            query=query,
            body=body,
        )

    def post_workflows_cron_parse(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /workflows/cron/parse."""
        return self._request(
            Operation("POST", "/workflows/cron/parse"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_workflows_cron_validate(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /workflows/cron/validate."""
        return self._request(
            Operation("POST", "/workflows/cron/validate"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_schedule(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /workflows/schedules."""
        return self._request(
            Operation("POST", "/workflows/schedules"),
            path_params=(),
            query=query,
            body=body,
        )

    def pause_schedule(
        self,
        schedule_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /workflows/schedules/{param}/pause."""
        return self._request(
            Operation("POST", "/workflows/schedules/{param}/pause"),
            path_params=(schedule_id,),
            query=query,
            body=body,
        )

    def resume_schedule(
        self,
        schedule_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /workflows/schedules/{param}/resume."""
        return self._request(
            Operation("POST", "/workflows/schedules/{param}/resume"),
            path_params=(schedule_id,),
            query=query,
            body=body,
        )

    def trigger_schedule(
        self,
        schedule_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /workflows/schedules/{param}/trigger."""
        return self._request(
            Operation("POST", "/workflows/schedules/{param}/trigger"),
            path_params=(schedule_id,),
            query=query,
            body=body,
        )

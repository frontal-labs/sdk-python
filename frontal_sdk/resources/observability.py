"""Typed API resource for the observability endpoints."""

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


class Observability(
    APIResource[JSONResultT, BytesResultT, StreamResultT],
    Generic[JSONResultT, BytesResultT, StreamResultT],
):
    """Methods for the observability API endpoints."""

    def delete_alert(
        self, alert_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /observability/alerts/{param}."""
        return self._request(
            Operation("DELETE", "/observability/alerts/{param}"),
            path_params=(alert_id,),
            query=query,
        )

    def delete_dashboard(
        self, dashboard_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /observability/dashboards/{param}."""
        return self._request(
            Operation("DELETE", "/observability/dashboards/{param}"),
            path_params=(dashboard_id,),
            query=query,
        )

    def list_alerts(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /observability/alerts."""
        return self._request(
            Operation("GET", "/observability/alerts"),
            path_params=(),
            query=query,
        )

    def list_incidents(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /observability/alerts/incidents."""
        return self._request(
            Operation("GET", "/observability/alerts/incidents"),
            path_params=(),
            query=query,
        )

    def list_dashboards(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /observability/dashboards."""
        return self._request(
            Operation("GET", "/observability/dashboards"),
            path_params=(),
            query=query,
        )

    def get_dashboard(
        self, dashboard_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /observability/dashboards/{param}."""
        return self._request(
            Operation("GET", "/observability/dashboards/{param}"),
            path_params=(dashboard_id,),
            query=query,
        )

    def list_stats(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /observability/events/stats."""
        return self._request(
            Operation("GET", "/observability/events/stats"),
            path_params=(),
            query=query,
        )

    def list_metrics(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /observability/metrics."""
        return self._request(
            Operation("GET", "/observability/metrics"),
            path_params=(),
            query=query,
        )

    def get_observability_metrics_list(
        self, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /observability/metrics/list."""
        return self._request(
            Operation("GET", "/observability/metrics/list"),
            path_params=(),
            query=query,
        )

    def list_traces(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /observability/traces."""
        return self._request(
            Operation("GET", "/observability/traces"),
            path_params=(),
            query=query,
        )

    def get_trace(
        self, trace_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /observability/traces/{param}."""
        return self._request(
            Operation("GET", "/observability/traces/{param}"),
            path_params=(trace_id,),
            query=query,
        )

    def create_alert(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /observability/alerts."""
        return self._request(
            Operation("POST", "/observability/alerts"),
            path_params=(),
            query=query,
            body=body,
        )

    def disable_alert(
        self,
        alert_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /observability/alerts/{param}/disable."""
        return self._request(
            Operation("POST", "/observability/alerts/{param}/disable"),
            path_params=(alert_id,),
            query=query,
            body=body,
        )

    def enable_alert(
        self,
        alert_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /observability/alerts/{param}/enable."""
        return self._request(
            Operation("POST", "/observability/alerts/{param}/enable"),
            path_params=(alert_id,),
            query=query,
            body=body,
        )

    def create_dashboard(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /observability/dashboards."""
        return self._request(
            Operation("POST", "/observability/dashboards"),
            path_params=(),
            query=query,
            body=body,
        )

    def share_dashboard(
        self,
        dashboard_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /observability/dashboards/{param}/share."""
        return self._request(
            Operation("POST", "/observability/dashboards/{param}/share"),
            path_params=(dashboard_id,),
            query=query,
            body=body,
        )

    def create_event(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /observability/events."""
        return self._request(
            Operation("POST", "/observability/events"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_observability_events_batch(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /observability/events/batch."""
        return self._request(
            Operation("POST", "/observability/events/batch"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_observability_logs_ingest(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /observability/logs/ingest."""
        return self._request(
            Operation("POST", "/observability/logs/ingest"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_observability_logs_query(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /observability/logs/query."""
        return self._request(
            Operation("POST", "/observability/logs/query"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_observability_metrics_ingest(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /observability/metrics/ingest."""
        return self._request(
            Operation("POST", "/observability/metrics/ingest"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_observability_traces_query(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /observability/traces/query."""
        return self._request(
            Operation("POST", "/observability/traces/query"),
            path_params=(),
            query=query,
            body=body,
        )

    def update_alert(
        self,
        alert_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call PUT /observability/alerts/{param}."""
        return self._request(
            Operation("PUT", "/observability/alerts/{param}"),
            path_params=(alert_id,),
            query=query,
            body=body,
        )

    def update_dashboard(
        self,
        dashboard_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call PUT /observability/dashboards/{param}."""
        return self._request(
            Operation("PUT", "/observability/dashboards/{param}"),
            path_params=(dashboard_id,),
            query=query,
            body=body,
        )

    def stream_observability_logs_stream(
        self, *, query: QueryParams | None = None
    ) -> StreamResultT:
        """Call STREAM /observability/logs/stream."""
        return self._stream(
            Operation("STREAM", "/observability/logs/stream"),
            path_params=(),
            query=query,
        )

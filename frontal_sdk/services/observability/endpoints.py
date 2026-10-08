"""Generated endpoint catalog for the observability service."""

from frontal_sdk.utils.operation import Endpoint


class ObservabilityEndpoint(Endpoint):
    """Known observability API operations."""

    DELETE_OBSERVABILITY_ALERTS_PARAM_1 = ("DELETE", "/observability/alerts/{param}")
    DELETE_OBSERVABILITY_DASHBOARDS_PARAM_1 = (
        "DELETE",
        "/observability/dashboards/{param}",
    )
    GET_OBSERVABILITY_ALERTS = ("GET", "/observability/alerts")
    GET_OBSERVABILITY_ALERTS_INCIDENTS = ("GET", "/observability/alerts/incidents")
    GET_OBSERVABILITY_DASHBOARDS = ("GET", "/observability/dashboards")
    GET_OBSERVABILITY_DASHBOARDS_PARAM_1 = ("GET", "/observability/dashboards/{param}")
    GET_OBSERVABILITY_EVENTS_STATS = ("GET", "/observability/events/stats")
    GET_OBSERVABILITY_METRICS = ("GET", "/observability/metrics")
    GET_OBSERVABILITY_METRICS_LIST = ("GET", "/observability/metrics/list")
    GET_OBSERVABILITY_TRACES = ("GET", "/observability/traces")
    GET_OBSERVABILITY_TRACES_PARAM_1 = ("GET", "/observability/traces/{param}")
    POST_OBSERVABILITY_ALERTS = ("POST", "/observability/alerts")
    POST_OBSERVABILITY_ALERTS_PARAM_1_DISABLE = (
        "POST",
        "/observability/alerts/{param}/disable",
    )
    POST_OBSERVABILITY_ALERTS_PARAM_1_ENABLE = (
        "POST",
        "/observability/alerts/{param}/enable",
    )
    POST_OBSERVABILITY_DASHBOARDS = ("POST", "/observability/dashboards")
    POST_OBSERVABILITY_DASHBOARDS_PARAM_1_SHARE = (
        "POST",
        "/observability/dashboards/{param}/share",
    )
    POST_OBSERVABILITY_EVENTS = ("POST", "/observability/events")
    POST_OBSERVABILITY_EVENTS_BATCH = ("POST", "/observability/events/batch")
    POST_OBSERVABILITY_LOGS_INGEST = ("POST", "/observability/logs/ingest")
    POST_OBSERVABILITY_LOGS_QUERY = ("POST", "/observability/logs/query")
    POST_OBSERVABILITY_METRICS_INGEST = ("POST", "/observability/metrics/ingest")
    POST_OBSERVABILITY_TRACES_QUERY = ("POST", "/observability/traces/query")
    PUT_OBSERVABILITY_ALERTS_PARAM_1 = ("PUT", "/observability/alerts/{param}")
    PUT_OBSERVABILITY_DASHBOARDS_PARAM_1 = ("PUT", "/observability/dashboards/{param}")
    STREAM_OBSERVABILITY_LOGS_STREAM = ("STREAM", "/observability/logs/stream")

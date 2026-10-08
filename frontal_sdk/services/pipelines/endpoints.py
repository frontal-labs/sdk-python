"""Generated endpoint catalog for the pipelines service."""

from frontal_sdk.utils.operation import Endpoint


class PipelinesEndpoint(Endpoint):
    """Known pipelines API operations."""

    GET_DATA_PIPELINES_CAPABILITIES = ("GET", "/data/pipelines/capabilities")
    GET_DATA_PIPELINES_HEALTH = ("GET", "/data/pipelines/health")
    GET_DATA_PIPELINES_INFO = ("GET", "/data/pipelines/info")
    GET_DATA_PIPELINES_PIPELINE_RUNS = ("GET", "/data/pipelines/pipeline-runs")
    GET_DATA_PIPELINES_PIPELINE_RUNS_PARAM_1 = (
        "GET",
        "/data/pipelines/pipeline-runs/{param}",
    )
    GET_DATA_PIPELINES_PIPELINES = ("GET", "/data/pipelines/pipelines")
    GET_DATA_PIPELINES_PIPELINES_PARAM_1 = ("GET", "/data/pipelines/pipelines/{param}")
    GET_DATA_PIPELINES_RUNS = ("GET", "/data/pipelines/runs")
    POST_DATA_PIPELINES_PIPELINES = ("POST", "/data/pipelines/pipelines")
    POST_DATA_PIPELINES_RUNS = ("POST", "/data/pipelines/runs")
    STREAM_DATA_PIPELINES_PIPELINE_RUNS_PARAM_1 = (
        "STREAM",
        "/data/pipelines/pipeline-runs/{param}",
    )

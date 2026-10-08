"""Generated endpoint catalog for the agents service."""

from frontal_sdk.utils.operation import Endpoint


class AgentsEndpoint(Endpoint):
    """Known agents API operations."""

    DELETE_AGENTS_PARAM_1 = ("DELETE", "/agents/{param}")
    GET_AGENTS = ("GET", "/agents")
    GET_AGENTS_PARAM_1 = ("GET", "/agents/{param}")
    GET_AGENTS_PARAM_1_RUNS = ("GET", "/agents/{param}/runs")
    GET_AGENTS_PARAM_1_VERSIONS = ("GET", "/agents/{param}/versions")
    GET_AGENTS_HEALTH = ("GET", "/agents/health")
    GET_AGENTS_RUNS_PARAM_1 = ("GET", "/agents/runs/{param}")
    GET_AGENTS_RUNS_PARAM_1_CONVERSATION = ("GET", "/agents/runs/{param}/conversation")
    POST_AGENTS = ("POST", "/agents")
    POST_AGENTS_PARAM_1_ROLLBACK = ("POST", "/agents/{param}/rollback")
    POST_AGENTS_PARAM_1_RUNS = ("POST", "/agents/{param}/runs")
    PUT_AGENTS_PARAM_1 = ("PUT", "/agents/{param}")
    STREAM_AGENTS_RUNS_PARAM_1_STREAM = ("STREAM", "/agents/runs/{param}/stream")

"""Generated endpoint catalog for the connectors service."""

from frontal_sdk.utils.operation import Endpoint


class ConnectorsEndpoint(Endpoint):
    """Known connectors API operations."""

    DELETE_CONNECTORS_INSTALLATIONS_PARAM_1 = (
        "DELETE",
        "/connectors/installations/{param}",
    )
    GET_CONNECTORS_CATALOG = ("GET", "/connectors/catalog")
    GET_CONNECTORS_CATALOG_PARAM_1 = ("GET", "/connectors/catalog/{param}")
    GET_CONNECTORS_CONNECTION_TESTS_PARAM_1 = (
        "GET",
        "/connectors/connection-tests/{param}",
    )
    GET_CONNECTORS_INSTALLATIONS = ("GET", "/connectors/installations")
    GET_CONNECTORS_INSTALLATIONS_PARAM_1 = ("GET", "/connectors/installations/{param}")
    GET_DIAGNOSTICS = ("GET", "/diagnostics")
    PATCH_CONNECTORS_INSTALLATIONS_PARAM_1 = (
        "PATCH",
        "/connectors/installations/{param}",
    )
    POST_CONNECTORS_INSTALLATIONS = ("POST", "/connectors/installations")
    POST_CONNECTORS_INSTALLATIONS_PARAM_1_PAUSE = (
        "POST",
        "/connectors/installations/{param}/pause",
    )
    POST_CONNECTORS_INSTALLATIONS_PARAM_1_RESUME = (
        "POST",
        "/connectors/installations/{param}/resume",
    )
    POST_CONNECTORS_SYNC_RUNS_PARAM_1_REPLAY = (
        "POST",
        "/connectors/sync-runs/{param}/replay",
    )

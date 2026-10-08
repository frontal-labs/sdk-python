"""Generated endpoint catalog for the schedules service."""

from frontal_sdk.utils.operation import Endpoint


class SchedulesEndpoint(Endpoint):
    """Known schedules API operations."""

    DELETE_WORKFLOWS_SCHEDULES_PARAM_1 = ("DELETE", "/workflows/schedules/{param}")
    GET_WORKFLOWS_SCHEDULES = ("GET", "/workflows/schedules")
    GET_WORKFLOWS_SCHEDULES_PARAM_1 = ("GET", "/workflows/schedules/{param}")
    PATCH_WORKFLOWS_SCHEDULES_PARAM_1 = ("PATCH", "/workflows/schedules/{param}")
    POST_WORKFLOWS_CRON_PARSE = ("POST", "/workflows/cron/parse")
    POST_WORKFLOWS_CRON_VALIDATE = ("POST", "/workflows/cron/validate")
    POST_WORKFLOWS_SCHEDULES = ("POST", "/workflows/schedules")
    POST_WORKFLOWS_SCHEDULES_PARAM_1_PAUSE = (
        "POST",
        "/workflows/schedules/{param}/pause",
    )
    POST_WORKFLOWS_SCHEDULES_PARAM_1_RESUME = (
        "POST",
        "/workflows/schedules/{param}/resume",
    )
    POST_WORKFLOWS_SCHEDULES_PARAM_1_TRIGGER = (
        "POST",
        "/workflows/schedules/{param}/trigger",
    )

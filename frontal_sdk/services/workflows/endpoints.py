"""Generated endpoint catalog for the workflows service."""

from frontal_sdk.utils.operation import Endpoint


class WorkflowsEndpoint(Endpoint):
    """Known workflows API operations."""

    DELETE_WORKFLOWS_PARAM_1 = ("DELETE", "/workflows/{param}")
    GET_WORKFLOWS = ("GET", "/workflows")
    GET_WORKFLOWS_PARAM_1 = ("GET", "/workflows/{param}")
    GET_WORKFLOWS_APPROVALS = ("GET", "/workflows/approvals")
    GET_WORKFLOWS_APPROVALS_PARAM_1 = ("GET", "/workflows/approvals/{param}")
    GET_WORKFLOWS_EXECUTIONS = ("GET", "/workflows/executions")
    GET_WORKFLOWS_EXECUTIONS_PARAM_1 = ("GET", "/workflows/executions/{param}")
    GET_WORKFLOWS_EXECUTIONS_PARAM_1_TASKS = (
        "GET",
        "/workflows/executions/{param}/tasks",
    )
    GET_WORKFLOWS_RUNS_PARAM_1_STEPS = ("GET", "/workflows/runs/{param}/steps")
    GET_WORKFLOWS_TASKS_PARAM_1 = ("GET", "/workflows/tasks/{param}")
    GET_WORKFLOWS_TEMPLATES = ("GET", "/workflows/templates")
    GET_WORKFLOWS_TEMPLATES_PARAM_1 = ("GET", "/workflows/templates/{param}")
    PATCH_WORKFLOWS_PARAM_1 = ("PATCH", "/workflows/{param}")
    POST_WORKFLOWS = ("POST", "/workflows")
    POST_WORKFLOWS_PARAM_1_ARCHIVE = ("POST", "/workflows/{param}/archive")
    POST_WORKFLOWS_PARAM_1_PUBLISH = ("POST", "/workflows/{param}/publish")
    POST_WORKFLOWS_PARAM_1_RESTORE = ("POST", "/workflows/{param}/restore")
    POST_WORKFLOWS_PARAM_1_VERSIONS = ("POST", "/workflows/{param}/versions")
    POST_WORKFLOWS_APPROVALS_PARAM_1_APPROVE = (
        "POST",
        "/workflows/approvals/{param}/approve",
    )
    POST_WORKFLOWS_APPROVALS_PARAM_1_REJECT = (
        "POST",
        "/workflows/approvals/{param}/reject",
    )
    POST_WORKFLOWS_EXECUTIONS = ("POST", "/workflows/executions")
    POST_WORKFLOWS_TASKS_PARAM_1_CANCEL = ("POST", "/workflows/tasks/{param}/cancel")
    POST_WORKFLOWS_TASKS_PARAM_1_RETRY = ("POST", "/workflows/tasks/{param}/retry")
    POST_WORKFLOWS_TEMPLATES = ("POST", "/workflows/templates")
    POST_WORKFLOWS_TEMPLATES_PARAM_1_INSTANTIATE = (
        "POST",
        "/workflows/templates/{param}/instantiate",
    )

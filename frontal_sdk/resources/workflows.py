"""Typed API resource for the workflows endpoints."""

from __future__ import annotations

import inspect
import unicodedata
from collections.abc import Awaitable, Callable, Mapping
from typing import Any, Generic, TypeVar, cast

from frontal_sdk.core.http import AsyncHttpClient
from frontal_sdk.core.operation import Operation
from frontal_sdk.core.polling import async_poll_until, poll_until
from frontal_sdk.models import (
    JSONValue,
    QueryParams,
    Workflow,
    WorkflowDefinition,
    WorkflowStep,
    WorkflowTrigger,
)
from frontal_sdk.models.requests import UNSET, RequestBodyInput
from frontal_sdk.resources._base import (
    APIResource,
    BytesResultT,
    HTTPTransport,
    JSONResultT,
    StreamResultT,
)

ResultT = TypeVar("ResultT")


class Workflows(
    APIResource[JSONResultT, BytesResultT, StreamResultT],
    Generic[JSONResultT, BytesResultT, StreamResultT],
):
    """Methods for the workflows API endpoints."""

    def __init__(
        self, http: HTTPTransport[JSONResultT, BytesResultT, StreamResultT]
    ) -> None:
        super().__init__(http)
        self.approvals = WorkflowApprovals(self)
        self.steps = WorkflowSteps(self)
        self.templates = WorkflowTemplates(self)

    def delete_workflow(
        self, workflow_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /workflows/{param}."""
        return self._request(
            Operation("DELETE", "/workflows/{param}"),
            path_params=(workflow_id,),
            query=query,
        )

    def list_workflows(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /workflows."""
        return self._request(
            Operation("GET", "/workflows"),
            path_params=(),
            query=query,
        )

    def get_workflow(
        self, workflow_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /workflows/{param}."""
        return self._request(
            Operation("GET", "/workflows/{param}"),
            path_params=(workflow_id,),
            query=query,
        )

    def list_approvals(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /workflows/approvals."""
        return self._request(
            Operation("GET", "/workflows/approvals"),
            path_params=(),
            query=query,
        )

    def get_approval(
        self, approval_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /workflows/approvals/{param}."""
        return self._request(
            Operation("GET", "/workflows/approvals/{param}"),
            path_params=(approval_id,),
            query=query,
        )

    def list_executions(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /workflows/executions."""
        return self._request(
            Operation("GET", "/workflows/executions"),
            path_params=(),
            query=query,
        )

    def get_execution(
        self, execution_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /workflows/executions/{param}."""
        return self._request(
            Operation("GET", "/workflows/executions/{param}"),
            path_params=(execution_id,),
            query=query,
        )

    def list_execution_tasks(
        self, execution_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /workflows/executions/{param}/tasks."""
        return self._request(
            Operation("GET", "/workflows/executions/{param}/tasks"),
            path_params=(execution_id,),
            query=query,
        )

    def list_run_steps(
        self, run_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /workflows/runs/{param}/steps."""
        return self._request(
            Operation("GET", "/workflows/runs/{param}/steps"),
            path_params=(run_id,),
            query=query,
        )

    def get_task(
        self, task_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /workflows/tasks/{param}."""
        return self._request(
            Operation("GET", "/workflows/tasks/{param}"),
            path_params=(task_id,),
            query=query,
        )

    def list_templates(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /workflows/templates."""
        return self._request(
            Operation("GET", "/workflows/templates"),
            path_params=(),
            query=query,
        )

    def get_template(
        self, template_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /workflows/templates/{param}."""
        return self._request(
            Operation("GET", "/workflows/templates/{param}"),
            path_params=(template_id,),
            query=query,
        )

    def update_workflow(
        self,
        workflow_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call PATCH /workflows/{param}."""
        return self._request(
            Operation("PATCH", "/workflows/{param}"),
            path_params=(workflow_id,),
            query=query,
            body=body,
        )

    def create_workflow(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /workflows."""
        return self._request(
            Operation("POST", "/workflows"),
            path_params=(),
            query=query,
            body=body,
        )

    def archive_workflow(
        self,
        workflow_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /workflows/{param}/archive."""
        return self._request(
            Operation("POST", "/workflows/{param}/archive"),
            path_params=(workflow_id,),
            query=query,
            body=body,
        )

    def publish_workflow(
        self,
        workflow_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /workflows/{param}/publish."""
        return self._request(
            Operation("POST", "/workflows/{param}/publish"),
            path_params=(workflow_id,),
            query=query,
            body=body,
        )

    def restore_workflow(
        self,
        workflow_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /workflows/{param}/restore."""
        return self._request(
            Operation("POST", "/workflows/{param}/restore"),
            path_params=(workflow_id,),
            query=query,
            body=body,
        )

    def create_version_for_workflow(
        self,
        workflow_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /workflows/{param}/versions."""
        return self._request(
            Operation("POST", "/workflows/{param}/versions"),
            path_params=(workflow_id,),
            query=query,
            body=body,
        )

    def approve_approval(
        self,
        approval_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /workflows/approvals/{param}/approve."""
        return self._request(
            Operation("POST", "/workflows/approvals/{param}/approve"),
            path_params=(approval_id,),
            query=query,
            body=body,
        )

    def reject_approval(
        self,
        approval_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /workflows/approvals/{param}/reject."""
        return self._request(
            Operation("POST", "/workflows/approvals/{param}/reject"),
            path_params=(approval_id,),
            query=query,
            body=body,
        )

    def create_execution(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /workflows/executions."""
        return self._request(
            Operation("POST", "/workflows/executions"),
            path_params=(),
            query=query,
            body=body,
        )

    def cancel_task(
        self,
        task_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /workflows/tasks/{param}/cancel."""
        return self._request(
            Operation("POST", "/workflows/tasks/{param}/cancel"),
            path_params=(task_id,),
            query=query,
            body=body,
        )

    def retry_task(
        self,
        task_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /workflows/tasks/{param}/retry."""
        return self._request(
            Operation("POST", "/workflows/tasks/{param}/retry"),
            path_params=(task_id,),
            query=query,
            body=body,
        )

    def create_template(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /workflows/templates."""
        return self._request(
            Operation("POST", "/workflows/templates"),
            path_params=(),
            query=query,
            body=body,
        )

    def instantiate_template(
        self,
        template_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /workflows/templates/{param}/instantiate."""
        return self._request(
            Operation("POST", "/workflows/templates/{param}/instantiate"),
            path_params=(template_id,),
            query=query,
            body=body,
        )

    def define(
        self, name: str
    ) -> WorkflowBuilder[JSONResultT, BytesResultT, StreamResultT]:
        """Start a validated workflow definition."""
        return WorkflowBuilder(self, name)

    def use(
        self, workflow_id: str
    ) -> WorkflowAccessor[JSONResultT, BytesResultT, StreamResultT]:
        """Create an accessor for one workflow and its executions."""
        return WorkflowAccessor(self, workflow_id)

    def list(
        self,
        *,
        status: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> JSONResultT:
        """List workflows using the service's cursor query names."""
        query: dict[str, str | int] = {}
        if status is not None:
            query["status"] = status
        if limit is not None:
            query["pageSize"] = limit
        if cursor is not None:
            query["pageToken"] = cursor
        return self.list_workflows(query=query)

    def create(
        self, definition: WorkflowDefinition | Mapping[str, JSONValue]
    ) -> JSONResultT:
        """Validate, create, and version a workflow definition."""
        model = _workflow_definition(definition)
        payload = cast(
            JSONValue, model.model_dump(mode="json", by_alias=True, exclude_none=True)
        )
        base: dict[str, JSONValue] = {
            "name": model.name,
            "slug": _slug(model.name),
        }
        if model.description is not None:
            base["description"] = model.description
        created = self.create_workflow(body=base)
        return _flat_map(
            created,
            lambda raw: self._create_version(raw, model, payload),
        )

    def _create_version(
        self,
        created: JSONValue,
        definition: WorkflowDefinition,
        payload: JSONValue,
    ) -> JSONResultT:
        workflow_data = _unwrap_record(created, "workflow")
        workflow_id = _resource_id(workflow_data, "workflowId")
        version_result = self.create_version_for_workflow(
            workflow_id, body={"spec": payload}
        )
        return _map_result(
            version_result,
            lambda version_raw: _workflow_json(
                workflow_data,
                _unwrap_record(version_raw, "version"),
                definition,
            ),
        )

    def _activate_created(self, created: JSONValue) -> JSONResultT:
        workflow_data = _unwrap_record(created, "workflow")
        workflow_id = _resource_id(workflow_data, "workflowId")
        return self.publish_workflow(workflow_id, body={})


def _workflow_definition(
    definition: WorkflowDefinition | Mapping[str, JSONValue],
) -> WorkflowDefinition:
    if isinstance(definition, WorkflowDefinition):
        return definition
    return WorkflowDefinition.model_validate(definition)


def _slug(name: str) -> str:
    ascii_name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return "-".join(
        part
        for part in "".join(
            char.lower() if char.isalnum() else " " for char in ascii_name
        ).split()
        if part
    )


def _unwrap_record(value: JSONValue, key: str) -> dict[str, JSONValue]:
    if not isinstance(value, dict):
        return {}
    nested = value.get(key)
    return nested if isinstance(nested, dict) else value


def _resource_id(record: Mapping[str, JSONValue], wire_key: str) -> str:
    value = record.get("id", record.get(wire_key))
    if not isinstance(value, str) or not value:
        raise ValueError(f"The API response did not contain {wire_key}")
    return value


def _map_result(result: ResultT, mapper: Callable[[JSONValue], JSONValue]) -> ResultT:
    if inspect.isawaitable(result):

        async def map_async() -> JSONValue:
            return mapper(await cast(Awaitable[JSONValue], result))

        return cast(ResultT, map_async())
    return cast(ResultT, mapper(cast(JSONValue, result)))


def _flat_map(result: ResultT, mapper: Callable[[JSONValue], ResultT]) -> ResultT:
    if inspect.isawaitable(result):

        async def flat_map_async() -> JSONValue:
            next_result = mapper(await cast(Awaitable[JSONValue], result))
            if inspect.isawaitable(next_result):
                return await cast(Awaitable[JSONValue], next_result)
            return cast(JSONValue, next_result)

        return cast(ResultT, flat_map_async())
    return mapper(cast(JSONValue, result))


def _workflow_json(
    created: Mapping[str, JSONValue],
    version: Mapping[str, JSONValue],
    definition: WorkflowDefinition,
) -> JSONValue:
    record: dict[str, JSONValue] = {**created, **version}
    record.update(
        cast(
            dict[str, JSONValue],
            definition.model_dump(mode="json", by_alias=True, exclude_none=True),
        )
    )
    record["id"] = _resource_id(created, "workflowId")
    record["status"] = str(record.get("status", "draft")).lower()
    latest_version = version.get("latestVersion", created.get("latestVersion"))
    if latest_version is None:
        latest_version = created.get("version", 1)
    record["version"] = latest_version
    workflow = Workflow.model_validate(record)
    return cast(
        JSONValue, workflow.model_dump(mode="json", by_alias=True, exclude_none=True)
    )


def _page_query(
    *, status: str | None = None, limit: int | None = None, cursor: str | None = None
) -> dict[str, str | int]:
    query: dict[str, str | int] = {}
    if status is not None:
        query["status"] = status
    if limit is not None:
        query["pageSize"] = limit
    if cursor is not None:
        query["pageToken"] = cursor
    return query


class WorkflowBuilder(Generic[JSONResultT, BytesResultT, StreamResultT]):
    """Fluent, Pydantic-validated workflow definition builder."""

    def __init__(
        self,
        workflows: Workflows[JSONResultT, BytesResultT, StreamResultT],
        name: str,
    ) -> None:
        self._workflows = workflows
        self._values: dict[str, JSONValue] = {
            "name": name,
            "triggers": [],
            "steps": [],
            "tags": [],
        }

    def description(
        self, text: str
    ) -> WorkflowBuilder[JSONResultT, BytesResultT, StreamResultT]:
        self._values["description"] = text
        return self

    def version(
        self, version: str
    ) -> WorkflowBuilder[JSONResultT, BytesResultT, StreamResultT]:
        self._values["version"] = version
        return self

    def variables(
        self, variables: Mapping[str, JSONValue]
    ) -> WorkflowBuilder[JSONResultT, BytesResultT, StreamResultT]:
        self._values["variables"] = dict(variables)
        return self

    def tags(
        self, *tags: str
    ) -> WorkflowBuilder[JSONResultT, BytesResultT, StreamResultT]:
        current = cast(list[JSONValue], self._values["tags"])
        self._values["tags"] = [*current, *tags]
        return self

    def trigger(
        self, trigger: WorkflowTrigger | Mapping[str, JSONValue]
    ) -> WorkflowBuilder[JSONResultT, BytesResultT, StreamResultT]:
        value = _model_value(trigger)
        cast(list[JSONValue], self._values["triggers"]).append(value)
        return self

    def manual(self) -> WorkflowBuilder[JSONResultT, BytesResultT, StreamResultT]:
        return self.trigger({"type": "manual"})

    def schedule(
        self, cron: str
    ) -> WorkflowBuilder[JSONResultT, BytesResultT, StreamResultT]:
        return self.trigger({"type": "schedule", "schedule": cron})

    def event(
        self, event_type: str, config: Mapping[str, JSONValue] | None = None
    ) -> WorkflowBuilder[JSONResultT, BytesResultT, StreamResultT]:
        value: dict[str, JSONValue] = {"type": "event", "eventType": event_type}
        if config is not None:
            value["config"] = dict(config)
        return self.trigger(value)

    def webhook(
        self, url: str
    ) -> WorkflowBuilder[JSONResultT, BytesResultT, StreamResultT]:
        return self.trigger({"type": "webhook", "webhookUrl": url})

    def step(
        self, step: WorkflowStep | Mapping[str, JSONValue]
    ) -> WorkflowBuilder[JSONResultT, BytesResultT, StreamResultT]:
        cast(list[JSONValue], self._values["steps"]).append(_model_value(step))
        return self

    def task(
        self,
        step_id: str,
        config: Mapping[str, JSONValue] | None = None,
        *,
        name: str | None = None,
        description: str | None = None,
        depends_on: list[str] | None = None,
        timeout: str | None = None,
    ) -> WorkflowBuilder[JSONResultT, BytesResultT, StreamResultT]:
        return self._append_step(
            {
                "id": step_id,
                "type": "task",
                "config": dict(config or {}),
                **_step_options(name, description, depends_on, timeout),
            }
        )

    def approval(
        self,
        step_id: str,
        approvers: list[str],
        *,
        name: str | None = None,
        description: str | None = None,
        depends_on: list[str] | None = None,
        timeout: str | None = None,
    ) -> WorkflowBuilder[JSONResultT, BytesResultT, StreamResultT]:
        return self._append_step(
            {
                "id": step_id,
                "type": "approval",
                "config": {"approvers": cast(JSONValue, approvers)},
                **_step_options(name, description, depends_on, timeout),
            }
        )

    def condition(
        self,
        step_id: str,
        expression: str,
        *,
        name: str | None = None,
        description: str | None = None,
        depends_on: list[str] | None = None,
    ) -> WorkflowBuilder[JSONResultT, BytesResultT, StreamResultT]:
        return self._append_step(
            {
                "id": step_id,
                "type": "condition",
                "condition": expression,
                **_step_options(name, description, depends_on, None),
            }
        )

    def parallel(
        self,
        step_id: str,
        steps: list[str],
        *,
        name: str | None = None,
        description: str | None = None,
        depends_on: list[str] | None = None,
    ) -> WorkflowBuilder[JSONResultT, BytesResultT, StreamResultT]:
        return self._append_step(
            {
                "id": step_id,
                "type": "parallel",
                "config": {"steps": cast(JSONValue, steps)},
                **_step_options(name, description, depends_on, None),
            }
        )

    def delay(
        self,
        step_id: str,
        duration: str,
        *,
        name: str | None = None,
        description: str | None = None,
        depends_on: list[str] | None = None,
    ) -> WorkflowBuilder[JSONResultT, BytesResultT, StreamResultT]:
        return self._append_step(
            {
                "id": step_id,
                "type": "delay",
                "config": {"duration": duration},
                **_step_options(name, description, depends_on, None),
            }
        )

    def notification(
        self,
        step_id: str,
        message: str,
        channels: list[str],
        *,
        name: str | None = None,
        description: str | None = None,
        depends_on: list[str] | None = None,
    ) -> WorkflowBuilder[JSONResultT, BytesResultT, StreamResultT]:
        return self._append_step(
            {
                "id": step_id,
                "type": "notification",
                "config": {
                    "message": message,
                    "channels": cast(JSONValue, channels),
                },
                **_step_options(name, description, depends_on, None),
            }
        )

    def _append_step(
        self, step: dict[str, JSONValue]
    ) -> WorkflowBuilder[JSONResultT, BytesResultT, StreamResultT]:
        cast(list[JSONValue], self._values["steps"]).append(step)
        return self

    def to_model(self) -> WorkflowDefinition:
        """Validate the collected triggers and steps before any network call."""
        return WorkflowDefinition.model_validate(self._values)

    def create(self) -> JSONResultT:
        """Create the workflow and its first version."""
        return self._workflows.create(self.to_model())

    def activate(self) -> JSONResultT:
        """Create and immediately publish the workflow."""
        return _flat_map(self.create(), self._workflows._activate_created)


class WorkflowAccessor(Generic[JSONResultT, BytesResultT, StreamResultT]):
    """Convenience operations for one workflow and its executions."""

    def __init__(
        self,
        workflows: Workflows[JSONResultT, BytesResultT, StreamResultT],
        workflow_id: str,
    ) -> None:
        self._workflows = workflows
        self.id = workflow_id

    def get(self) -> JSONResultT:
        return self._workflows.get_workflow(self.id)

    def update(self, definition: Mapping[str, JSONValue]) -> JSONResultT:
        return self._workflows.update_workflow(self.id, body=dict(definition))

    def delete(self) -> JSONResultT:
        return self._workflows.delete_workflow(self.id)

    def activate(self) -> JSONResultT:
        return self._workflows.publish_workflow(self.id, body={})

    def archive(self) -> JSONResultT:
        return self._workflows.archive_workflow(self.id, body={})

    def restore(self) -> JSONResultT:
        return self._workflows.restore_workflow(self.id, body={})

    def executions(
        self,
        *,
        status: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> JSONResultT:
        query = _page_query(status=status, limit=limit, cursor=cursor)
        query["workflowId"] = self.id
        return self._workflows.list_executions(query=query)

    def execution(self, execution_id: str) -> JSONResultT:
        return self._workflows.get_execution(execution_id)

    def trigger(self, input: Mapping[str, JSONValue] | None = None) -> JSONResultT:
        return self._workflows.create_execution(
            body={"workflowId": self.id, "input": dict(input or {})}
        )

    def wait_for_completion(
        self,
        execution_id: str,
        *,
        interval: float = 2.0,
        timeout: float = 300.0,
    ) -> JSONResultT:
        """Poll until an execution reaches completed, failed, or cancelled."""
        if isinstance(self._workflows._http, AsyncHttpClient):

            async def fetch() -> JSONValue:
                result = self.execution(execution_id)
                return await cast(Awaitable[JSONValue], result)

            result = async_poll_until(
                fetch,
                until=_is_terminal_execution,
                interval=interval,
                timeout=timeout,
            )
            return cast(JSONResultT, result)

        result = poll_until(
            lambda: cast(JSONValue, self.execution(execution_id)),
            until=_is_terminal_execution,
            interval=interval,
            timeout=timeout,
        )
        return cast(JSONResultT, result)


def _is_terminal_execution(value: JSONValue) -> bool:
    execution = _unwrap_record(value, "execution")
    status = execution.get("status")
    return isinstance(status, str) and status.lower() in {
        "completed",
        "failed",
        "cancelled",
    }


def _model_value(value: Any) -> JSONValue:
    if hasattr(value, "model_dump"):
        value = value.model_dump(mode="json", by_alias=True, exclude_none=True)
    return cast(JSONValue, value)


def _step_options(
    name: str | None,
    description: str | None,
    depends_on: list[str] | None,
    timeout: str | None,
) -> dict[str, JSONValue]:
    options: dict[str, JSONValue] = {}
    for key, value in (
        ("name", name),
        ("description", description),
        ("dependsOn", depends_on),
        ("timeout", timeout),
    ):
        if value is not None:
            options[key] = cast(JSONValue, value)
    return options


class WorkflowApprovals(Generic[JSONResultT, BytesResultT, StreamResultT]):
    """Approval operations exposed as ``workflows.approvals``."""

    def __init__(
        self, workflows: Workflows[JSONResultT, BytesResultT, StreamResultT]
    ) -> None:
        self._workflows = workflows

    def list(
        self,
        *,
        status: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> JSONResultT:
        return self._workflows.list_approvals(
            query=_page_query(status=status, limit=limit, cursor=cursor)
        )

    def get(self, approval_id: str) -> JSONResultT:
        return self._workflows.get_approval(approval_id)

    def approve(self, approval_id: str, comment: str | None = None) -> JSONResultT:
        body: dict[str, JSONValue] = {} if comment is None else {"comment": comment}
        return self._workflows.approve_approval(approval_id, body=body)

    def reject(self, approval_id: str, comment: str | None = None) -> JSONResultT:
        body: dict[str, JSONValue] = {} if comment is None else {"comment": comment}
        return self._workflows.reject_approval(approval_id, body=body)


class WorkflowSteps(Generic[JSONResultT, BytesResultT, StreamResultT]):
    """Task and run step operations exposed as ``workflows.steps``."""

    def __init__(
        self, workflows: Workflows[JSONResultT, BytesResultT, StreamResultT]
    ) -> None:
        self._workflows = workflows

    def list_tasks(
        self,
        execution_id: str,
        *,
        status: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> JSONResultT:
        return self._workflows.list_execution_tasks(
            execution_id, query=_page_query(status=status, limit=limit, cursor=cursor)
        )

    def get_task(self, task_id: str) -> JSONResultT:
        return self._workflows.get_task(task_id)

    def retry_task(self, task_id: str) -> JSONResultT:
        return self._workflows.retry_task(task_id, body={})

    def cancel_task(self, task_id: str, reason: str | None = None) -> JSONResultT:
        body: dict[str, JSONValue] = {} if reason is None else {"reason": reason}
        return self._workflows.cancel_task(task_id, body=body)

    def list_run_steps(
        self,
        run_id: str,
        *,
        status: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> JSONResultT:
        return self._workflows.list_run_steps(
            run_id, query=_page_query(status=status, limit=limit, cursor=cursor)
        )


class WorkflowTemplates(Generic[JSONResultT, BytesResultT, StreamResultT]):
    """Template operations exposed as ``workflows.templates``."""

    def __init__(
        self, workflows: Workflows[JSONResultT, BytesResultT, StreamResultT]
    ) -> None:
        self._workflows = workflows

    def list(
        self,
        *,
        category: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> JSONResultT:
        query = _page_query(limit=limit, cursor=cursor)
        if category is not None:
            query["category"] = category
        return self._workflows.list_templates(query=query)

    def get(self, template_id: str) -> JSONResultT:
        return self._workflows.get_template(template_id)

    def create(
        self,
        *,
        name: str,
        definition: WorkflowDefinition | Mapping[str, JSONValue],
        description: str | None = None,
        category: str | None = None,
    ) -> JSONResultT:
        model = _workflow_definition(definition)
        body: dict[str, JSONValue] = {
            "name": name,
            "definition": cast(
                JSONValue,
                model.model_dump(mode="json", by_alias=True, exclude_none=True),
            ),
        }
        if description is not None:
            body["description"] = description
        if category is not None:
            body["category"] = category
        return self._workflows.create_template(body=body)

    def use(self, template_id: str, name: str) -> JSONResultT:
        return self._workflows.instantiate_template(template_id, body={"name": name})


__all__ = [
    "WorkflowAccessor",
    "WorkflowApprovals",
    "WorkflowBuilder",
    "WorkflowSteps",
    "WorkflowTemplates",
    "Workflows",
]

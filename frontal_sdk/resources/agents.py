"""Typed API resource for the agents endpoints."""

from __future__ import annotations

import inspect
import time
from collections.abc import Awaitable, Callable, Mapping
from math import isfinite
from typing import Any, Generic, Optional, cast

import anyio

from frontal_sdk.core.errors import TimeoutError as FrontalTimeoutError
from frontal_sdk.core.operation import Operation
from frontal_sdk.models import (
    AgentDefinition,
    AgentRateLimit,
    AgentScope,
    AgentTrigger,
    ConfidenceConfig,
    JSONValue,
    MemoryConfig,
    QueryParams,
    RetryConfig,
)
from frontal_sdk.models.requests import UNSET, RequestBodyInput
from frontal_sdk.resources._base import (
    APIResource,
    BytesResultT,
    HTTPTransport,
    JSONResultT,
    StreamResultT,
)


class Agents(
    APIResource[JSONResultT, BytesResultT, StreamResultT],
    Generic[JSONResultT, BytesResultT, StreamResultT],
):
    """Methods for the agents API endpoints."""

    def __init__(
        self, http: HTTPTransport[JSONResultT, BytesResultT, StreamResultT]
    ) -> None:
        super().__init__(http)
        self.runs = AgentRuns(self)
        self.versions = AgentVersions(self)

    def _delete_agent(
        self, agent_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /agents/{param}."""
        return self._request(
            Operation("DELETE", "/agents/{param}"),
            path_params=(agent_id,),
            query=query,
        )

    def _list_agents(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /agents."""
        return self._request(
            Operation("GET", "/agents"),
            path_params=(),
            query=query,
        )

    def _get_agent(
        self, agent_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /agents/{param}."""
        return self._request(
            Operation("GET", "/agents/{param}"),
            path_params=(agent_id,),
            query=query,
        )

    def _list_agent_runs(
        self, agent_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /agents/{param}/runs."""
        return self._request(
            Operation("GET", "/agents/{param}/runs"),
            path_params=(agent_id,),
            query=query,
        )

    def _list_agent_versions(
        self, agent_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /agents/{param}/versions."""
        return self._request(
            Operation("GET", "/agents/{param}/versions"),
            path_params=(agent_id,),
            query=query,
        )

    def _get_agents_health(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /agents/health."""
        return self._request(
            Operation("GET", "/agents/health"),
            path_params=(),
            query=query,
        )

    def _get_run(self, run_id: str, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /agents/runs/{param}."""
        return self._request(
            Operation("GET", "/agents/runs/{param}"),
            path_params=(run_id,),
            query=query,
        )

    def _get_run_conversation(
        self, run_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /agents/runs/{param}/conversation."""
        return self._request(
            Operation("GET", "/agents/runs/{param}/conversation"),
            path_params=(run_id,),
            query=query,
        )

    def _create_agent(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /agents."""
        return self._request(
            Operation("POST", "/agents"),
            path_params=(),
            query=query,
            body=body,
        )

    def _rollback_agent(
        self,
        agent_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /agents/{param}/rollback."""
        return self._request(
            Operation("POST", "/agents/{param}/rollback"),
            path_params=(agent_id,),
            query=query,
            body=body,
        )

    def _create_run_for_agent(
        self,
        agent_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /agents/{param}/runs."""
        return self._request(
            Operation("POST", "/agents/{param}/runs"),
            path_params=(agent_id,),
            query=query,
            body=body,
        )

    def _update_agent(
        self,
        agent_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call PUT /agents/{param}."""
        return self._request(
            Operation("PUT", "/agents/{param}"),
            path_params=(agent_id,),
            query=query,
            body=body,
        )

    def _stream_run(
        self, run_id: str, *, query: QueryParams | None = None
    ) -> StreamResultT:
        """Call STREAM /agents/runs/{param}/stream."""
        return self._stream(
            Operation("STREAM", "/agents/runs/{param}/stream"),
            path_params=(run_id,),
            query=query,
        )

    def define(
        self,
        name: str,
        options: AgentDefinition | Mapping[str, JSONValue] | None = None,
    ) -> AgentBuilder[JSONResultT, BytesResultT, StreamResultT]:
        """Start a fluent agent definition; call ``create()`` to send it."""
        builder = AgentBuilder(self, name)
        if options is not None:
            builder.configure(options)
        return builder

    def use(
        self,
        agent_id: str,
        *,
        approve_when: Callable[[JSONValue], bool] | None = None,
        approvers: list[str] | None = None,
    ) -> AgentAccessor[JSONResultT, BytesResultT, StreamResultT]:
        """Create an accessor for one agent and its runs."""
        return AgentAccessor(self, agent_id, approve_when, approvers)

    def get(self, id: str, *, query: QueryParams | None = None) -> JSONResultT:
        """Retrieve one agent."""
        return self._get_agent(id, query=query)

    def list(self, *, query: QueryParams | None = None) -> JSONResultT:
        """List agents using the endpoint's query parameters."""
        return self._list_agents(query=query)

    def create(
        self,
        *,
        body: RequestBodyInput = UNSET,
        query: QueryParams | None = None,
    ) -> JSONResultT:
        """Create one agent, serializing an AgentDefinition when provided."""
        if isinstance(body, AgentDefinition):
            body = cast(
                JSONValue,
                body.model_dump(mode="json", by_alias=True, exclude_none=True),
            )
        return self._create_agent(body=body, query=query)

    def update(
        self,
        id: str,
        *,
        body: RequestBodyInput = UNSET,
        query: QueryParams | None = None,
    ) -> JSONResultT:
        """Replace an agent definition."""
        return self._update_agent(id, body=body, query=query)

    def delete(self, id: str, *, query: QueryParams | None = None) -> JSONResultT:
        """Delete one agent."""
        return self._delete_agent(id, query=query)

    def rollback(
        self,
        id: str,
        *,
        body: RequestBodyInput = UNSET,
        query: QueryParams | None = None,
    ) -> JSONResultT:
        """Roll back an agent to a prior version."""
        return self._rollback_agent(id, body=body, query=query)

    def health(self) -> JSONResultT:
        """Check the agent service health."""
        return self._get_agents_health()


class AgentRuns(Generic[JSONResultT, BytesResultT, StreamResultT]):
    """Run operations scoped under ``client.agents.runs``."""

    def __init__(
        self, agents: Agents[JSONResultT, BytesResultT, StreamResultT]
    ) -> None:
        self._agents = agents

    def list(self, *, agent_id: str, query: QueryParams | None = None) -> JSONResultT:
        return self._agents._list_agent_runs(agent_id, query=query)

    def create(
        self,
        *,
        agent_id: str,
        body: RequestBodyInput = UNSET,
        query: QueryParams | None = None,
    ) -> JSONResultT:
        return self._agents._create_run_for_agent(agent_id, body=body, query=query)

    def get(self, id: str, *, query: QueryParams | None = None) -> JSONResultT:
        return self._agents._get_run(id, query=query)

    def conversation(self, id: str, *, query: QueryParams | None = None) -> JSONResultT:
        return self._agents._get_run_conversation(id, query=query)

    def stream(self, id: str, *, query: QueryParams | None = None) -> StreamResultT:
        return self._agents._stream_run(id, query=query)


class AgentVersions(Generic[JSONResultT, BytesResultT, StreamResultT]):
    """Version operations scoped under ``client.agents.versions``."""

    def __init__(
        self, agents: Agents[JSONResultT, BytesResultT, StreamResultT]
    ) -> None:
        self._agents = agents

    def list(self, *, agent_id: str, query: QueryParams | None = None) -> JSONResultT:
        return self._agents._list_agent_versions(agent_id, query=query)


class AgentBuilder(Generic[JSONResultT, BytesResultT, StreamResultT]):
    """Fluent, Pydantic-validated builder for an agent definition."""

    def __init__(
        self,
        agents: Agents[JSONResultT, BytesResultT, StreamResultT],
        name: str,
    ) -> None:
        self._agents = agents
        self._values: dict[str, JSONValue] = {"name": name, "triggers": [], "tags": []}
        self._scope = AgentScope()
        self._confidence = ConfidenceConfig()
        self._memory = MemoryConfig()
        self._retry = RetryConfig()

    def configure(
        self, definition: AgentDefinition | Mapping[str, JSONValue]
    ) -> AgentBuilder[JSONResultT, BytesResultT, StreamResultT]:
        """Apply request fields from a Pydantic model or mapping."""
        if isinstance(definition, AgentDefinition):
            values = definition.model_dump(
                mode="json", by_alias=True, exclude_none=True
            )
        else:
            values = dict(definition)
        name = values.get("name")
        if isinstance(name, str):
            self._values["name"] = name
        description = values.get("description")
        if isinstance(description, str):
            self.description(description)
        trigger_values = values.get("triggers")
        if isinstance(trigger_values, (str, list)):
            raw_triggers: list[object] = (
                [trigger_values]
                if isinstance(trigger_values, str)
                else cast(list[object], trigger_values)
            )
            for item in raw_triggers:
                trigger = AgentTrigger.model_validate(
                    {"event": item} if isinstance(item, str) else cast(Any, item)
                )
                event_filter = (
                    trigger.filter if isinstance(trigger.filter, Mapping) else None
                )
                self.trigger(
                    trigger.event,
                    cast(Optional[Mapping[str, JSONValue]], event_filter),
                )
        tags = values.get("tags")
        if isinstance(tags, list):
            self.tags(*[tag for tag in tags if isinstance(tag, str)])
        if "scope" in values:
            self.scope(cast(Mapping[str, JSONValue], values["scope"]))
        if "confidence" in values:
            self.confidence(cast(Mapping[str, JSONValue], values["confidence"]))
        if "memory" in values:
            self.memory(cast(Mapping[str, JSONValue], values["memory"]))
        if "retry" in values:
            self.retry(cast(Mapping[str, JSONValue], values["retry"]))
        timeout = values.get("timeout")
        if isinstance(timeout, str):
            self.timeout(timeout)
        rate_limit = values.get("rateLimit")
        if isinstance(rate_limit, Mapping):
            self.rate_limit(cast(Mapping[str, JSONValue], rate_limit))
        return self

    def description(
        self, text: str
    ) -> AgentBuilder[JSONResultT, BytesResultT, StreamResultT]:
        self._values["description"] = text
        return self

    def trigger(
        self, event: str, filter: Mapping[str, JSONValue] | None = None
    ) -> AgentBuilder[JSONResultT, BytesResultT, StreamResultT]:
        triggers = cast(list[JSONValue], self._values["triggers"])
        trigger: dict[str, JSONValue] = {"event": event}
        if filter is not None:
            trigger["filter"] = dict(filter)
        triggers.append(trigger)
        return self

    def scope(
        self, value: AgentScope | Mapping[str, JSONValue]
    ) -> AgentBuilder[JSONResultT, BytesResultT, StreamResultT]:
        self._scope = (
            value if isinstance(value, AgentScope) else AgentScope.model_validate(value)
        )
        return self

    def can_read(
        self, *entity_types: str
    ) -> AgentBuilder[JSONResultT, BytesResultT, StreamResultT]:
        self._scope.read.extend(entity_types)
        return self

    def can_write(
        self, *entity_types: str
    ) -> AgentBuilder[JSONResultT, BytesResultT, StreamResultT]:
        self._scope.write.extend(entity_types)
        return self

    def can_invoke(
        self, *actions: str
    ) -> AgentBuilder[JSONResultT, BytesResultT, StreamResultT]:
        self._scope.actions.extend(actions)
        return self

    def escalates_on(
        self, *conditions: str
    ) -> AgentBuilder[JSONResultT, BytesResultT, StreamResultT]:
        self._scope.escalate.extend(conditions)
        return self

    def confidence(
        self, value: ConfidenceConfig | Mapping[str, JSONValue]
    ) -> AgentBuilder[JSONResultT, BytesResultT, StreamResultT]:
        self._confidence = (
            value
            if isinstance(value, ConfidenceConfig)
            else ConfidenceConfig.model_validate(value)
        )
        return self

    def auto_execute_above(
        self, threshold: float
    ) -> AgentBuilder[JSONResultT, BytesResultT, StreamResultT]:
        self._confidence.auto_execute_above = threshold
        return self

    def escalate_below(
        self, threshold: float
    ) -> AgentBuilder[JSONResultT, BytesResultT, StreamResultT]:
        self._confidence.escalate_below = threshold
        return self

    def memory(
        self, value: MemoryConfig | Mapping[str, JSONValue]
    ) -> AgentBuilder[JSONResultT, BytesResultT, StreamResultT]:
        self._memory = (
            value
            if isinstance(value, MemoryConfig)
            else MemoryConfig.model_validate(value)
        )
        return self

    def retry(
        self, value: RetryConfig | Mapping[str, JSONValue]
    ) -> AgentBuilder[JSONResultT, BytesResultT, StreamResultT]:
        self._retry = (
            value
            if isinstance(value, RetryConfig)
            else RetryConfig.model_validate(value)
        )
        return self

    def timeout(
        self, duration: str
    ) -> AgentBuilder[JSONResultT, BytesResultT, StreamResultT]:
        self._values["timeout"] = duration
        return self

    def rate_limit(
        self, value: AgentRateLimit | Mapping[str, JSONValue]
    ) -> AgentBuilder[JSONResultT, BytesResultT, StreamResultT]:
        model = (
            value
            if isinstance(value, AgentRateLimit)
            else AgentRateLimit.model_validate(value)
        )
        self._values["rateLimit"] = cast(
            JSONValue, model.model_dump(mode="json", by_alias=True)
        )
        return self

    def tags(
        self, *tags: str
    ) -> AgentBuilder[JSONResultT, BytesResultT, StreamResultT]:
        self._values["tags"] = [*cast(list[str], self._values["tags"]), *tags]
        return self

    def to_model(self) -> AgentDefinition:
        """Validate the accumulated definition and apply schema defaults."""
        values: dict[str, object] = {
            **self._values,
            "scope": self._scope,
            "confidence": self._confidence,
            "memory": self._memory,
            "retry": self._retry,
        }
        return AgentDefinition.model_validate(values)

    def to_json(self) -> dict[str, JSONValue]:
        """Return a JSON-ready, validated agent definition."""
        return cast(
            dict[str, JSONValue],
            self.to_model().model_dump(mode="json", by_alias=True, exclude_none=True),
        )

    def create(self) -> JSONResultT:
        """Validate and create the agent on the configured client."""
        return self._agents.create(body=self.to_model())


class AgentAccessor(Generic[JSONResultT, BytesResultT, StreamResultT]):
    """Convenience methods for one agent and its runs."""

    def __init__(
        self,
        agents: Agents[JSONResultT, BytesResultT, StreamResultT],
        agent_id: str,
        approve_when: Callable[[JSONValue], bool] | None = None,
        approvers: list[str] | None = None,
    ) -> None:
        self._agents = agents
        self.id = agent_id
        self._approve_when = approve_when
        self.approvers = list(approvers or [])

    def requires_approval(self, state: JSONValue) -> bool:
        """Evaluate the optional local approval predicate for a run state."""
        return self._approve_when(state) if self._approve_when is not None else False

    def get(self) -> JSONResultT:
        return self._agents.get(id=self.id)

    def update(self, definition: Mapping[str, JSONValue]) -> JSONResultT:
        return self._agents.update(id=self.id, body=dict(definition))

    def delete(self) -> JSONResultT:
        return self._agents.delete(id=self.id)

    def rollback(self, *, to_version: int | None = None) -> JSONResultT:
        body: dict[str, JSONValue] = {}
        if to_version is not None:
            body["toVersion"] = to_version
        return self._agents.rollback(self.id, body=body)

    def versions(
        self, *, limit: int | None = None, cursor: str | None = None
    ) -> JSONResultT:
        query: dict[str, str | int] = {}
        if limit is not None:
            query["limit"] = limit
        if cursor is not None:
            query["cursor"] = cursor
        return self._agents.versions.list(agent_id=self.id, query=query)

    def runs(
        self,
        *,
        status: str | None = None,
        from_time: str | None = None,
        to_time: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> JSONResultT:
        query: dict[str, str | int] = {}
        for key, value in (
            ("status", status),
            ("from", from_time),
            ("to", to_time),
            ("limit", limit),
            ("cursor", cursor),
        ):
            if value is not None:
                query[key] = value
        return self._agents.runs.list(agent_id=self.id, query=query)

    def run(self, run_id: str) -> JSONResultT:
        return self._agents.runs.get(run_id)

    def wait_for_completion(
        self,
        run_id: str,
        *,
        interval: float = 2.0,
        timeout: float | None = 300.0,
    ) -> JSONResultT:
        """Poll a run until it completes, fails, or is escalated.

        This returns a normal value for ``Frontal`` and an awaitable for
        ``AsyncFrontal``. The async client never blocks the event loop.
        """
        if not isfinite(interval) or interval <= 0:
            raise ValueError("interval must be a finite positive number")
        if timeout is not None and (not isfinite(timeout) or timeout <= 0):
            raise ValueError("timeout must be a finite positive number")
        started = time.monotonic()
        first = self.run(run_id)
        if inspect.isawaitable(first):

            async def wait_async(initial: Awaitable[JSONValue]) -> JSONValue:
                current = await initial
                while not _terminal_run(current):
                    remaining = _remaining_time(started, timeout)
                    await anyio.sleep(
                        interval if remaining is None else min(interval, remaining)
                    )
                    next_result = cast(Awaitable[JSONValue], self.run(run_id))
                    current = await next_result
                return current

            return cast(JSONResultT, wait_async(cast(Awaitable[JSONValue], first)))

        current = cast(JSONValue, first)
        while not _terminal_run(current):
            remaining = _remaining_time(started, timeout)
            time.sleep(interval if remaining is None else min(interval, remaining))
            current = cast(JSONValue, self.run(run_id))
        return cast(JSONResultT, current)

    def conversation(self, run_id: str) -> JSONResultT:
        return self._agents.runs.conversation(run_id)

    def message(self, event: str, payload: Mapping[str, JSONValue]) -> JSONResultT:
        body: dict[str, JSONValue] = {"event": event, "payload": dict(payload)}
        return self._agents.runs.create(agent_id=self.id, body=body)

    def watch(self, run_id: str) -> StreamResultT:
        """Watch a run as a sync iterator or async iterator of server events."""
        return self._agents.runs.stream(run_id)


def _terminal_run(value: JSONValue) -> bool:
    if isinstance(value, dict):
        execution = value.get("execution", value)
        if isinstance(execution, dict):
            return str(execution.get("status", "")).lower() in {
                "completed",
                "failed",
                "escalated",
            }
    return False


def _remaining_time(started: float, timeout: float | None) -> float | None:
    if timeout is None:
        return None
    remaining = timeout - (time.monotonic() - started)
    if remaining <= 0:
        raise FrontalTimeoutError("Timed out waiting for agent run completion")
    return remaining


__all__ = ["AgentAccessor", "AgentBuilder", "Agents"]

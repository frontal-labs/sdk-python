"""Typed API resource for the agents endpoints."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Generic, cast

from frontal_sdk.core.operation import Operation
from frontal_sdk.models import (
    AgentDefinition,
    AgentRateLimit,
    AgentScope,
    ConfidenceConfig,
    JSONValue,
    MemoryConfig,
    QueryParams,
    RequestBody,
    RetryConfig,
)
from frontal_sdk.resources._base import (
    APIResource,
    BytesResultT,
    JSONResultT,
    StreamResultT,
)


class Agents(
    APIResource[JSONResultT, BytesResultT, StreamResultT],
    Generic[JSONResultT, BytesResultT, StreamResultT],
):
    """Methods for the agents API endpoints."""

    def delete_agents_by_param_1(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /agents/{param}."""
        return self._request(
            Operation("DELETE", "/agents/{param}"),
            path_params=(param_1,),
            query=query,
        )

    def get_agents(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /agents."""
        return self._request(
            Operation("GET", "/agents"),
            path_params=(),
            query=query,
        )

    def get_agents_by_param_1(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /agents/{param}."""
        return self._request(
            Operation("GET", "/agents/{param}"),
            path_params=(param_1,),
            query=query,
        )

    def get_agents_by_param_1_runs(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /agents/{param}/runs."""
        return self._request(
            Operation("GET", "/agents/{param}/runs"),
            path_params=(param_1,),
            query=query,
        )

    def get_agents_by_param_1_versions(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /agents/{param}/versions."""
        return self._request(
            Operation("GET", "/agents/{param}/versions"),
            path_params=(param_1,),
            query=query,
        )

    def get_agents_health(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /agents/health."""
        return self._request(
            Operation("GET", "/agents/health"),
            path_params=(),
            query=query,
        )

    def get_agents_runs_by_param_1(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /agents/runs/{param}."""
        return self._request(
            Operation("GET", "/agents/runs/{param}"),
            path_params=(param_1,),
            query=query,
        )

    def get_agents_runs_by_param_1_conversation(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /agents/runs/{param}/conversation."""
        return self._request(
            Operation("GET", "/agents/runs/{param}/conversation"),
            path_params=(param_1,),
            query=query,
        )

    def post_agents(
        self, *, query: QueryParams | None = None, body: RequestBody = None
    ) -> JSONResultT:
        """Call POST /agents."""
        return self._request(
            Operation("POST", "/agents"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_agents_by_param_1_rollback(
        self,
        param_1: str,
        *,
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONResultT:
        """Call POST /agents/{param}/rollback."""
        return self._request(
            Operation("POST", "/agents/{param}/rollback"),
            path_params=(param_1,),
            query=query,
            body=body,
        )

    def post_agents_by_param_1_runs(
        self,
        param_1: str,
        *,
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONResultT:
        """Call POST /agents/{param}/runs."""
        return self._request(
            Operation("POST", "/agents/{param}/runs"),
            path_params=(param_1,),
            query=query,
            body=body,
        )

    def put_agents_by_param_1(
        self,
        param_1: str,
        *,
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONResultT:
        """Call PUT /agents/{param}."""
        return self._request(
            Operation("PUT", "/agents/{param}"),
            path_params=(param_1,),
            query=query,
            body=body,
        )

    def stream_agents_runs_by_param_1_stream(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> StreamResultT:
        """Call STREAM /agents/runs/{param}/stream."""
        return self._stream(
            Operation("STREAM", "/agents/runs/{param}/stream"),
            path_params=(param_1,),
            query=query,
        )

    def define(
        self, name: str
    ) -> AgentBuilder[JSONResultT, BytesResultT, StreamResultT]:
        """Start a fluent agent definition; call ``create()`` to send it."""
        return AgentBuilder(self, name)

    def use(
        self, agent_id: str
    ) -> AgentAccessor[JSONResultT, BytesResultT, StreamResultT]:
        """Create an accessor for one agent and its runs."""
        return AgentAccessor(self, agent_id)

    def list(
        self,
        *,
        status: str | None = None,
        trigger: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> JSONResultT:
        """List agents with the filters and cursor used by the TypeScript SDK."""
        query: dict[str, str | int] = {}
        if status is not None:
            query["status"] = status
        if trigger is not None:
            query["trigger"] = trigger
        if limit is not None:
            query["limit"] = limit
        if cursor is not None:
            query["cursor"] = cursor
        return self.get_agents(query=query)

    def create(
        self, definition: AgentDefinition | Mapping[str, JSONValue]
    ) -> JSONResultT:
        """Validate and create an agent definition."""
        model = (
            definition
            if isinstance(definition, AgentDefinition)
            else AgentDefinition.model_validate(definition)
        )
        body = cast(
            JSONValue, model.model_dump(mode="json", by_alias=True, exclude_none=True)
        )
        return self.post_agents(body=body)

    def health(self) -> JSONResultT:
        """Check the agent service health."""
        return self.get_agents_health()


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

    def create(self) -> JSONResultT:
        """Validate and create the agent on the configured client."""
        return self._agents.create(self.to_model())


class AgentAccessor(Generic[JSONResultT, BytesResultT, StreamResultT]):
    """Convenience methods for one agent and its runs."""

    def __init__(
        self,
        agents: Agents[JSONResultT, BytesResultT, StreamResultT],
        agent_id: str,
    ) -> None:
        self._agents = agents
        self.id = agent_id

    def get(self) -> JSONResultT:
        return self._agents.get_agents_by_param_1(self.id)

    def update(self, definition: Mapping[str, JSONValue]) -> JSONResultT:
        return self._agents.put_agents_by_param_1(self.id, body=dict(definition))

    def delete(self) -> JSONResultT:
        return self._agents.delete_agents_by_param_1(self.id)

    def rollback(self, *, to_version: int | None = None) -> JSONResultT:
        body: dict[str, JSONValue] = {}
        if to_version is not None:
            body["toVersion"] = to_version
        return self._agents.post_agents_by_param_1_rollback(self.id, body=body)

    def versions(
        self, *, limit: int | None = None, cursor: str | None = None
    ) -> JSONResultT:
        query: dict[str, str | int] = {}
        if limit is not None:
            query["limit"] = limit
        if cursor is not None:
            query["cursor"] = cursor
        return self._agents.get_agents_by_param_1_versions(self.id, query=query)

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
        return self._agents.get_agents_by_param_1_runs(self.id, query=query)

    def run(self, run_id: str) -> JSONResultT:
        return self._agents.get_agents_runs_by_param_1(run_id)

    def conversation(self, run_id: str) -> JSONResultT:
        return self._agents.get_agents_runs_by_param_1_conversation(run_id)

    def message(self, event: str, payload: Mapping[str, JSONValue]) -> JSONResultT:
        body: dict[str, JSONValue] = {"event": event, "payload": dict(payload)}
        return self._agents.post_agents_by_param_1_runs(self.id, body=body)

    def watch(self, run_id: str) -> StreamResultT:
        """Watch a run as a sync iterator or async iterator of server events."""
        return self._agents.stream_agents_runs_by_param_1_stream(run_id)


__all__ = ["AgentAccessor", "AgentBuilder", "Agents"]

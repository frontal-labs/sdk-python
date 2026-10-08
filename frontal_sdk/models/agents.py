"""Pydantic models for agent definitions and runtime records."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import ConfigDict, Field

from frontal_sdk.models.ai import AIModel
from frontal_sdk.models.types import APIModel, JSONValue


class AgentTrigger(APIModel):
    """Event that can start an agent run."""

    event: str
    filter: JSONValue = None
    debounce: str | None = None


class AgentScope(APIModel):
    """Resource permissions granted to an agent."""

    read: list[str] = Field(default_factory=list)
    write: list[str] = Field(default_factory=list)
    actions: list[str] = Field(default_factory=list)
    escalate: list[str] = Field(default_factory=list)
    invoke_agents: list[str] = Field(default_factory=list, alias="invokeAgents")
    invoke_functions: list[str] = Field(default_factory=list, alias="invokeFunctions")


class ConfidenceConfig(APIModel):
    """Confidence thresholds for auto-execution and review."""

    auto_execute_above: float = Field(
        default=0.85, alias="autoExecuteAbove", ge=0, le=1
    )
    escalate_below: float = Field(default=0.6, alias="escalateBelow", ge=0, le=1)
    require_review_between: bool = Field(default=True, alias="requireReviewBetween")


class MemoryConfig(APIModel):
    """Memory policy for an agent."""

    type: Literal["working", "persistent", "episodic"] = "working"
    ttl: str | None = None
    max_tokens: int | None = Field(default=None, alias="maxTokens", gt=0)


class RetryConfig(APIModel):
    """Agent retry policy."""

    max_retries: int = Field(default=3, alias="maxRetries", ge=0)
    retry_delay: int = Field(default=1000, alias="retryDelay", gt=0)
    backoff: Literal["constant", "linear", "exponential"] = "exponential"
    retry_on: list[int] = Field(
        default_factory=lambda: [408, 409, 425, 429, 500, 502, 503, 504],
        alias="retryOn",
    )


class AgentRateLimit(APIModel):
    """Optional per-agent concurrency and execution limits."""

    max_executions_per_minute: int | None = Field(
        default=None, alias="maxExecutionsPerMinute", gt=0
    )
    max_concurrent: int | None = Field(default=None, alias="maxConcurrent", gt=0)


class AgentDefinition(APIModel):
    """Validated payload used to create an agent."""

    name: str = Field(min_length=1)
    description: str | None = None
    triggers: list[AgentTrigger] = Field(min_length=1)
    scope: AgentScope = Field(default_factory=AgentScope)
    confidence: ConfidenceConfig = Field(default_factory=ConfidenceConfig)
    memory: MemoryConfig = Field(default_factory=MemoryConfig)
    retry: RetryConfig = Field(default_factory=RetryConfig)
    timeout: str = "30s"
    rate_limit: AgentRateLimit | None = Field(default=None, alias="rateLimit")
    tags: list[str] = Field(default_factory=list)


class AgentMetricsSummary(AIModel):
    """Optional aggregate runtime metrics for an agent."""

    executions_today: int = Field(alias="executionsToday")
    escalation_rate: float = Field(alias="escalationRate", ge=0, le=1)
    avg_execution_ms: int = Field(alias="avgExecutionMs")
    success_rate: float = Field(alias="successRate", ge=0, le=1)


class Agent(AgentDefinition):
    """Agent resource and its current runtime state."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    version: int
    status: Literal["draft", "active", "paused", "deprecated"]
    environment: str
    metrics: AgentMetricsSummary | None = None
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class AgentExecution(AIModel):
    """An agent run and its trigger details."""

    id: str
    agent_id: str = Field(alias="agentId")
    trigger_event: str = Field(alias="triggerEvent")
    trigger_payload: dict[str, JSONValue] = Field(alias="triggerPayload")
    status: Literal["running", "completed", "failed", "escalated"]
    outcome: str | None = None
    confidence: float | None = Field(default=None, ge=0, le=1)
    decision_trace: list[JSONValue] | None = Field(default=None, alias="decisionTrace")
    actions_taken: list[JSONValue] | None = Field(default=None, alias="actionsTaken")
    escalation_id: str | None = Field(default=None, alias="escalationId")
    started_at: datetime = Field(alias="startedAt")
    completed_at: datetime | None = Field(default=None, alias="completedAt")
    duration_ms: int | None = Field(default=None, alias="durationMs")
    error: str | None = None


__all__ = [
    "Agent",
    "AgentDefinition",
    "AgentExecution",
    "AgentMetricsSummary",
    "AgentRateLimit",
    "AgentScope",
    "AgentTrigger",
    "ConfidenceConfig",
    "MemoryConfig",
    "RetryConfig",
]

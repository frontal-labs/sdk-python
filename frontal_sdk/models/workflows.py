"""Pydantic models for workflow definitions and runtime records."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal, Union

from pydantic import ConfigDict, Field

from frontal_sdk.models.ai import AIModel
from frontal_sdk.models.types import APIModel, JSONValue

WorkflowStatus = Literal["draft", "active", "archived"]
ExecutionStatus = Literal["pending", "running", "completed", "failed", "cancelled"]
StepStatus = Literal["pending", "running", "completed", "failed", "skipped"]
ApprovalStatus = Literal["pending", "approved", "rejected", "cancelled", "expired"]
StepType = Literal["task", "approval", "condition", "parallel", "delay", "notification"]


class ManualTrigger(APIModel):
    type: Literal["manual"]
    config: dict[str, JSONValue] | None = None


class ScheduleTrigger(APIModel):
    type: Literal["schedule"]
    schedule: str
    config: dict[str, JSONValue] | None = None


class EventTrigger(APIModel):
    type: Literal["event"]
    event_type: str = Field(alias="eventType")
    config: dict[str, JSONValue] | None = None


class WebhookTrigger(APIModel):
    type: Literal["webhook"]
    webhook_url: str = Field(alias="webhookUrl")
    config: dict[str, JSONValue] | None = None


WorkflowTrigger = Annotated[
    Union[ManualTrigger, ScheduleTrigger, EventTrigger, WebhookTrigger],
    Field(discriminator="type"),
]


class StepRetryPolicy(APIModel):
    max_attempts: int | None = Field(default=None, alias="maxAttempts", gt=0)
    backoff: Literal["linear", "exponential"] | None = None


class StepFields(APIModel):
    id: str
    name: str | None = None
    description: str | None = None
    depends_on: list[str] | None = Field(default=None, alias="dependsOn")
    timeout: str | None = None
    retry_policy: StepRetryPolicy | None = Field(default=None, alias="retryPolicy")


class TaskStep(StepFields):
    type: Literal["task"]
    config: dict[str, JSONValue]


class ApprovalStepConfig(AIModel):
    approvers: list[str]


class ApprovalStep(StepFields):
    type: Literal["approval"]
    config: ApprovalStepConfig


class ConditionStep(StepFields):
    type: Literal["condition"]
    condition: str


class ParallelStepConfig(AIModel):
    steps: list[str]


class ParallelStep(StepFields):
    type: Literal["parallel"]
    config: ParallelStepConfig


class DelayStepConfig(AIModel):
    duration: str


class DelayStep(StepFields):
    type: Literal["delay"]
    config: DelayStepConfig


class NotificationStepConfig(AIModel):
    message: str
    channels: list[str]


class NotificationStep(StepFields):
    type: Literal["notification"]
    config: NotificationStepConfig


WorkflowStep = Annotated[
    Union[
        TaskStep,
        ApprovalStep,
        ConditionStep,
        ParallelStep,
        DelayStep,
        NotificationStep,
    ],
    Field(discriminator="type"),
]


class WorkflowDefinition(APIModel):
    """Validated input used to create or update a workflow version."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    name: str = Field(min_length=1)
    description: str | None = None
    version: str | None = None
    triggers: list[WorkflowTrigger] = Field(min_length=1)
    steps: list[WorkflowStep] = Field(min_length=1)
    variables: dict[str, JSONValue] | None = None
    tags: list[str] = Field(default_factory=list)


class Workflow(AIModel):
    """Workflow resource and lifecycle state."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    name: str
    description: str | None = None
    status: WorkflowStatus
    version: int | None = None
    latest_version: int | None = Field(default=None, alias="latestVersion")
    triggers: list[WorkflowTrigger] | None = None
    steps: list[WorkflowStep] | None = None
    variables: dict[str, JSONValue] | None = None
    tags: list[str] | None = None
    created_at: datetime | None = Field(default=None, alias="createdAt")
    updated_at: datetime | None = Field(default=None, alias="updatedAt")


class WorkflowStepExecution(AIModel):
    """Execution result for one workflow step."""

    step_id: str = Field(alias="stepId")
    status: StepStatus
    input: dict[str, JSONValue] | None = None
    output: dict[str, JSONValue] | None = None
    started_at: datetime | None = Field(default=None, alias="startedAt")
    completed_at: datetime | None = Field(default=None, alias="completedAt")
    duration_ms: int | None = Field(default=None, alias="durationMs")
    error: str | None = None
    retry_count: int = Field(default=0, alias="retryCount")


class WorkflowExecution(AIModel):
    """Workflow execution and its step-level results."""

    id: str
    workflow_id: str = Field(alias="workflowId")
    status: ExecutionStatus
    workflow_version: int | None = Field(default=None, alias="workflowVersion")
    input: dict[str, JSONValue] | None = None
    output: dict[str, JSONValue] | None = None
    variables: dict[str, JSONValue] | None = None
    step_executions: list[WorkflowStepExecution] | None = Field(
        default=None, alias="stepExecutions"
    )
    triggered_by: str | None = Field(default=None, alias="triggeredBy")
    started_at: datetime | None = Field(default=None, alias="startedAt")
    completed_at: datetime | None = Field(default=None, alias="completedAt")
    duration_ms: int | None = Field(default=None, alias="durationMs")
    error: str | None = None


class StepDefinition(AIModel):
    """Standalone workflow step payload used by step APIs."""

    id: str
    type: StepType
    name: str | None = None
    description: str | None = None
    config: dict[str, JSONValue] | None = None
    timeout: str | None = None
    retry_policy: StepRetryPolicy | None = Field(default=None, alias="retryPolicy")


class Approval(AIModel):
    """Human approval request attached to a workflow execution."""

    id: str
    execution_id: str = Field(alias="executionId")
    step_id: str = Field(alias="stepId")
    status: ApprovalStatus
    signal_name: str = Field(alias="signalName")
    title: str
    description: str
    required_approvers: list[str] = Field(alias="requiredApprovers")
    approved_by: list[str] = Field(alias="approvedBy")
    rejected_by: str | None = Field(default=None, alias="rejectedBy")
    cancel_reason: str | None = Field(default=None, alias="cancelReason")
    comment: str | None = None
    expires_at: datetime | None = Field(default=None, alias="expiresAt")
    resolved_at: datetime | None = Field(default=None, alias="resolvedAt")
    created_by: str = Field(alias="createdBy")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class WorkflowTask(AIModel):
    """Task instance produced by a workflow execution."""

    id: str
    task_id: str | None = Field(default=None, alias="taskId")
    step_id: str = Field(alias="stepId")
    execution_id: str = Field(alias="executionId")
    status: str
    type: str
    attempt: int
    max_attempts: int = Field(alias="maxAttempts")
    input: dict[str, JSONValue] | None = None
    output: dict[str, JSONValue] | None = None
    error: dict[str, JSONValue] | None = None
    error_message: str | None = Field(default=None, alias="errorMessage")
    started_at: datetime | None = Field(default=None, alias="startedAt")
    completed_at: datetime | None = Field(default=None, alias="completedAt")
    created_at: datetime | None = Field(default=None, alias="createdAt")
    updated_at: datetime | None = Field(default=None, alias="updatedAt")


class WorkflowRunStep(AIModel):
    """Projected workflow run step with timing and retry details."""

    step_id: str = Field(alias="stepId")
    step_index: int = Field(alias="stepIndex")
    status: str
    input: dict[str, JSONValue] | None = None
    output: dict[str, JSONValue] | None = None
    error: dict[str, JSONValue] | None = None
    attempt: int
    max_attempts: int = Field(alias="maxAttempts")
    latency_ms: float | None = Field(default=None, alias="latencyMs")
    started_at: datetime | None = Field(default=None, alias="startedAt")
    completed_at: datetime | None = Field(default=None, alias="completedAt")


class WorkflowTemplate(AIModel):
    """Reusable workflow definition template."""

    id: str
    name: str
    description: str | None = None
    category: str | None = None
    definition: dict[str, JSONValue]
    tags: list[str] = Field(default_factory=list)
    created_by: str | None = Field(default=None, alias="createdBy")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


__all__ = [
    "Approval",
    "ApprovalStatus",
    "ApprovalStep",
    "ApprovalStepConfig",
    "ConditionStep",
    "DelayStep",
    "DelayStepConfig",
    "EventTrigger",
    "ExecutionStatus",
    "ManualTrigger",
    "NotificationStep",
    "NotificationStepConfig",
    "ParallelStep",
    "ParallelStepConfig",
    "ScheduleTrigger",
    "StepDefinition",
    "StepRetryPolicy",
    "StepStatus",
    "StepType",
    "TaskStep",
    "WebhookTrigger",
    "Workflow",
    "WorkflowDefinition",
    "WorkflowExecution",
    "WorkflowRunStep",
    "WorkflowStatus",
    "WorkflowStep",
    "WorkflowStepExecution",
    "WorkflowTask",
    "WorkflowTemplate",
    "WorkflowTrigger",
]

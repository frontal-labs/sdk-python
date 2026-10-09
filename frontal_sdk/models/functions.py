"""Pydantic models for the Frontal Functions service."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import ConfigDict, Field

from frontal_sdk.models.types import APIModel, JSONObject, JSONValue

FunctionRuntime = Literal["nodejs20", "nodejs22", "python311"]
FunctionStatus = Literal["draft", "active", "deprecated", "failed"]


class FunctionPermission(APIModel):
    """Ontology and action permissions assigned to a function."""

    ontology: list[str] | None = None
    actions: list[str] | None = None


class FunctionDefinition(APIModel):
    """Validated payload used to create or update a function."""

    name: str = Field(min_length=1)
    runtime: FunctionRuntime
    entrypoint: str
    description: str | None = None
    source: str | None = None
    input_schema: JSONObject | None = Field(default=None, alias="inputSchema")
    output_schema: JSONObject | None = Field(default=None, alias="outputSchema")
    dependencies: list[str] | None = None
    env_vars: dict[str, str] | None = Field(default=None, alias="envVars")
    secrets: list[str] | None = None
    memory: int | None = Field(default=None, gt=0)
    timeout: int | None = Field(default=None, gt=0)
    permissions: FunctionPermission | None = None


class FunctionResource(APIModel):
    """Function resource and its current lifecycle state."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    name: str
    runtime: FunctionRuntime
    entrypoint: str
    status: FunctionStatus
    version: int = Field(gt=0)
    description: str | None = None
    latest_version: int | None = Field(default=None, alias="latestVersion", gt=0)
    memory: int | None = Field(default=None, gt=0)
    timeout: int | None = Field(default=None, gt=0)
    permissions: FunctionPermission | None = None
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class FunctionVersion(APIModel):
    """Published or draft source version of a function."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    version: int = Field(gt=0)
    source: str
    created_at: datetime = Field(alias="createdAt")
    published_by: str | None = Field(default=None, alias="publishedBy")


class FunctionExecution(APIModel):
    """Status and JSON input/output for one function execution."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    function_id: str = Field(alias="functionId")
    version: int = Field(gt=0)
    status: FunctionStatus
    input: JSONObject | None = None
    output: JSONObject | None = None
    error: str | None = None
    started_at: datetime | None = Field(default=None, alias="startedAt")
    completed_at: datetime | None = Field(default=None, alias="completedAt")
    duration_ms: int | None = Field(default=None, alias="durationMs", ge=0)


class FunctionInvocationInput(APIModel):
    """Request to invoke a function with an arbitrary JSON object."""

    function_id: str = Field(alias="functionId")
    version: int | None = Field(default=None, gt=0)
    input: JSONObject | None = None


class FunctionInvocationResult(APIModel):
    """Result of a synchronous or completed asynchronous invocation."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    execution_id: str = Field(alias="executionId")
    result: JSONObject | None = None
    error: str | None = None
    status: FunctionStatus | None = None


class FunctionInvocationAccepted(APIModel):
    """Execution identifier returned after an asynchronous invocation."""

    execution_id: str = Field(alias="executionId")


class FunctionDeploymentStatus(APIModel):
    """Deployment state and optional JSON details for a function version."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    status: str
    details: JSONValue = None


class FunctionPagination(APIModel):
    """Cursor metadata returned with function service list responses."""

    cursor: str | None = None
    has_more: bool = Field(alias="hasMore")


class FunctionListResponse(APIModel):
    """A page of functions."""

    functions: list[FunctionResource]
    pagination: FunctionPagination


class FunctionVersionListResponse(APIModel):
    """A page of function versions."""

    versions: list[FunctionVersion]
    pagination: FunctionPagination


class FunctionExecutionListResponse(APIModel):
    """A page of function executions."""

    executions: list[FunctionExecution]
    pagination: FunctionPagination


__all__ = [
    "FunctionDefinition",
    "FunctionDeploymentStatus",
    "FunctionExecution",
    "FunctionExecutionListResponse",
    "FunctionInvocationAccepted",
    "FunctionInvocationInput",
    "FunctionInvocationResult",
    "FunctionListResponse",
    "FunctionPagination",
    "FunctionPermission",
    "FunctionResource",
    "FunctionRuntime",
    "FunctionStatus",
    "FunctionVersion",
    "FunctionVersionListResponse",
]

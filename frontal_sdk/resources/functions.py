"""Typed API resources for the Frontal Functions service."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Generic, cast

from frontal_sdk.core.operation import Operation
from frontal_sdk.models import JSONValue, QueryParams
from frontal_sdk.models.functions import (
    FunctionDefinition,
    FunctionInvocationInput,
    FunctionPermission,
    FunctionRuntime,
)
from frontal_sdk.models.requests import RequestBodyInput
from frontal_sdk.resources._base import (
    APIResource,
    BytesResultT,
    HTTPTransport,
    JSONResultT,
    StreamResultT,
)


def _definition_model(
    definition: FunctionDefinition | Mapping[str, JSONValue],
) -> FunctionDefinition:
    if isinstance(definition, FunctionDefinition):
        return definition
    return FunctionDefinition.model_validate(definition)


def _invocation_model(
    value: FunctionInvocationInput | Mapping[str, JSONValue],
) -> FunctionInvocationInput:
    if isinstance(value, FunctionInvocationInput):
        return value
    return FunctionInvocationInput.model_validate(value)


def _model_payload(model: FunctionDefinition | FunctionInvocationInput) -> JSONValue:
    return cast(
        JSONValue,
        model.model_dump(mode="json", by_alias=True, exclude_none=True),
    )


class Functions(
    APIResource[JSONResultT, BytesResultT, StreamResultT],
    Generic[JSONResultT, BytesResultT, StreamResultT],
):
    """Function definitions, versions, deployments, and executions."""

    def __init__(
        self, http: HTTPTransport[JSONResultT, BytesResultT, StreamResultT]
    ) -> None:
        super().__init__(http)
        self.versions = FunctionVersions(self)
        self.deployments = FunctionDeployments(self)
        self.executions = FunctionExecutions(self)

    def _create_function(
        self, *, query: QueryParams | None = None, body: RequestBodyInput
    ) -> JSONResultT:
        """Call POST /functions."""
        return self._request(
            Operation("POST", "/functions"), path_params=(), query=query, body=body
        )

    def _list_functions(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /functions."""
        return self._request(Operation("GET", "/functions"), query=query)

    def _get_function(
        self, function_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /functions/{param}."""
        return self._request(
            Operation("GET", "/functions/{param}"),
            path_params=(function_id,),
            query=query,
        )

    def _update_function(
        self,
        function_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput,
    ) -> JSONResultT:
        """Call PATCH /functions/{param}."""
        return self._request(
            Operation("PATCH", "/functions/{param}"),
            path_params=(function_id,),
            query=query,
            body=body,
        )

    def _delete_function(
        self, function_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /functions/{param}."""
        return self._request(
            Operation("DELETE", "/functions/{param}"),
            path_params=(function_id,),
            query=query,
        )

    def _list_function_versions(
        self, function_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /functions/{param}/versions."""
        return self._request(
            Operation("GET", "/functions/{param}/versions"),
            path_params=(function_id,),
            query=query,
        )

    def _get_function_version(
        self,
        function_id: str,
        version: int,
        *,
        query: QueryParams | None = None,
    ) -> JSONResultT:
        """Call GET /functions/{param}/versions/{param}."""
        return self._request(
            Operation("GET", "/functions/{param}/versions/{param}"),
            path_params=(function_id, str(version)),
            query=query,
        )

    def _publish_function_version(
        self,
        function_id: str,
        version: int,
        *,
        query: QueryParams | None = None,
    ) -> JSONResultT:
        """Call POST /functions/{param}/versions/{param}/publish."""
        return self._request(
            Operation("POST", "/functions/{param}/versions/{param}/publish"),
            path_params=(function_id, str(version)),
            query=query,
            body={},
        )

    def _deploy_function_version(
        self,
        function_id: str,
        version: int,
        *,
        query: QueryParams | None = None,
    ) -> JSONResultT:
        """Call POST /functions/{param}/versions/{param}/deploy."""
        return self._request(
            Operation("POST", "/functions/{param}/versions/{param}/deploy"),
            path_params=(function_id, str(version)),
            query=query,
            body={},
        )

    def _get_function_deployment_status(
        self,
        function_id: str,
        version: int,
        *,
        query: QueryParams | None = None,
    ) -> JSONResultT:
        """Call GET /functions/{param}/versions/{param}/deployment/status."""
        return self._request(
            Operation("GET", "/functions/{param}/versions/{param}/deployment/status"),
            path_params=(function_id, str(version)),
            query=query,
        )

    def _invoke_function(
        self, *, query: QueryParams | None = None, body: RequestBodyInput
    ) -> JSONResultT:
        """Call POST /functions/invoke."""
        return self._request(
            Operation("POST", "/functions/invoke"), query=query, body=body
        )

    def _invoke_function_async(
        self, *, query: QueryParams | None = None, body: RequestBodyInput
    ) -> JSONResultT:
        """Call POST /functions/invoke-async."""
        return self._request(
            Operation("POST", "/functions/invoke-async"), query=query, body=body
        )

    def _get_function_execution(
        self, execution_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /functions/executions/{param}."""
        return self._request(
            Operation("GET", "/functions/executions/{param}"),
            path_params=(execution_id,),
            query=query,
        )

    def _get_function_execution_result(
        self, execution_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /functions/executions/{param}/result."""
        return self._request(
            Operation("GET", "/functions/executions/{param}/result"),
            path_params=(execution_id,),
            query=query,
        )

    def _list_function_executions(
        self, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /functions/executions."""
        return self._request(Operation("GET", "/functions/executions"), query=query)

    def _cancel_function_execution(
        self, execution_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call POST /functions/executions/{param}/cancel."""
        return self._request(
            Operation("POST", "/functions/executions/{param}/cancel"),
            path_params=(execution_id,),
            query=query,
            body={},
        )

    def create(
        self,
        definition: FunctionDefinition | Mapping[str, JSONValue],
        *,
        query: QueryParams | None = None,
    ) -> JSONResultT:
        """Validate and create a function definition."""
        return self._create_function(
            body=_model_payload(_definition_model(definition)), query=query
        )

    def list(self, *, query: QueryParams | None = None) -> JSONResultT:
        """List functions with optional ``cursor`` and ``limit`` query values."""
        return self._list_functions(query=query)

    def get(self, id: str, *, query: QueryParams | None = None) -> JSONResultT:
        """Retrieve one function by ID."""
        return self._get_function(id, query=query)

    def update(
        self,
        id: str,
        definition: FunctionDefinition | Mapping[str, JSONValue],
        *,
        query: QueryParams | None = None,
    ) -> JSONResultT:
        """Validate and patch a function definition, creating a version."""
        return self._update_function(
            id, body=_model_payload(_definition_model(definition)), query=query
        )

    def delete(self, id: str, *, query: QueryParams | None = None) -> JSONResultT:
        """Delete a function."""
        return self._delete_function(id, query=query)

    def define(
        self,
        name: str,
        options: FunctionDefinition | Mapping[str, JSONValue] | None = None,
    ) -> FunctionBuilder[JSONResultT, BytesResultT, StreamResultT]:
        """Start a fluent definition; call ``create()`` to send it."""
        builder = FunctionBuilder(self, name)
        if options is not None:
            builder.configure(options)
        return builder

    def use(
        self, function_id: str
    ) -> FunctionAccessor[JSONResultT, BytesResultT, StreamResultT]:
        """Create an accessor for one function."""
        return FunctionAccessor(self, function_id)


class FunctionVersions(Generic[JSONResultT, BytesResultT, StreamResultT]):
    """Version operations available under ``client.functions.versions``."""

    def __init__(self, functions: Functions[JSONResultT, BytesResultT, StreamResultT]):
        self._functions = functions

    def list(
        self, *, function_id: str, query: QueryParams | None = None
    ) -> JSONResultT:
        """List versions for one function."""
        return self._functions._list_function_versions(function_id, query=query)

    def get(
        self,
        function_id: str,
        version: int,
        *,
        query: QueryParams | None = None,
    ) -> JSONResultT:
        """Retrieve one version of a function."""
        return self._functions._get_function_version(function_id, version, query=query)

    def publish(
        self,
        function_id: str,
        version: int,
        *,
        query: QueryParams | None = None,
    ) -> JSONResultT:
        """Publish one version of a function."""
        return self._functions._publish_function_version(
            function_id, version, query=query
        )


class FunctionDeployments(Generic[JSONResultT, BytesResultT, StreamResultT]):
    """Deployment operations available under ``client.functions.deployments``."""

    def __init__(self, functions: Functions[JSONResultT, BytesResultT, StreamResultT]):
        self._functions = functions

    def deploy(
        self,
        function_id: str,
        version: int,
        *,
        query: QueryParams | None = None,
    ) -> JSONResultT:
        """Deploy one version of a function."""
        return self._functions._deploy_function_version(
            function_id, version, query=query
        )

    def status(
        self,
        function_id: str,
        version: int,
        *,
        query: QueryParams | None = None,
    ) -> JSONResultT:
        """Retrieve the deployment status of a function version."""
        return self._functions._get_function_deployment_status(
            function_id, version, query=query
        )


class FunctionExecutions(Generic[JSONResultT, BytesResultT, StreamResultT]):
    """Invocation and execution operations under ``client.functions.executions``."""

    def __init__(self, functions: Functions[JSONResultT, BytesResultT, StreamResultT]):
        self._functions = functions

    def invoke(
        self,
        input: FunctionInvocationInput | Mapping[str, JSONValue],
        *,
        query: QueryParams | None = None,
    ) -> JSONResultT:
        """Invoke a function and wait for its result."""
        payload = _model_payload(_invocation_model(input))
        return self._functions._invoke_function(body=payload, query=query)

    def invoke_async(
        self,
        input: FunctionInvocationInput | Mapping[str, JSONValue],
        *,
        query: QueryParams | None = None,
    ) -> JSONResultT:
        """Start an asynchronous function invocation."""
        payload = _model_payload(_invocation_model(input))
        return self._functions._invoke_function_async(body=payload, query=query)

    def get(
        self, execution_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Retrieve one function execution."""
        return self._functions._get_function_execution(execution_id, query=query)

    def get_result(
        self, execution_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Retrieve a function execution result."""
        return self._functions._get_function_execution_result(execution_id, query=query)

    def list(self, *, query: QueryParams | None = None) -> JSONResultT:
        """List executions, optionally filtering by cursor, function ID, or status."""
        return self._functions._list_function_executions(query=query)

    def cancel(
        self, execution_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Cancel one function execution."""
        return self._functions._cancel_function_execution(execution_id, query=query)


class FunctionBuilder(Generic[JSONResultT, BytesResultT, StreamResultT]):
    """Fluent, Pydantic-validated builder for a function definition."""

    def __init__(
        self,
        functions: Functions[JSONResultT, BytesResultT, StreamResultT],
        name: str,
    ) -> None:
        self._functions = functions
        self._values: dict[str, JSONValue] = {"name": name}

    def configure(
        self, definition: FunctionDefinition | Mapping[str, JSONValue]
    ) -> FunctionBuilder[JSONResultT, BytesResultT, StreamResultT]:
        """Apply fields from a model or a mapping to this builder."""
        if isinstance(definition, FunctionDefinition):
            values = cast(
                dict[str, JSONValue],
                definition.model_dump(mode="json", by_alias=True, exclude_none=True),
            )
        else:
            values = dict(definition)
        self._values.update(values)
        return self

    def description(
        self, text: str
    ) -> FunctionBuilder[JSONResultT, BytesResultT, StreamResultT]:
        self._values["description"] = text
        return self

    def runtime(
        self, runtime: FunctionRuntime
    ) -> FunctionBuilder[JSONResultT, BytesResultT, StreamResultT]:
        self._values["runtime"] = runtime
        return self

    def entrypoint(
        self, entrypoint: str
    ) -> FunctionBuilder[JSONResultT, BytesResultT, StreamResultT]:
        self._values["entrypoint"] = entrypoint
        return self

    def source(
        self, source: str
    ) -> FunctionBuilder[JSONResultT, BytesResultT, StreamResultT]:
        self._values["source"] = source
        return self

    def input_schema(
        self, schema: Mapping[str, JSONValue]
    ) -> FunctionBuilder[JSONResultT, BytesResultT, StreamResultT]:
        self._values["inputSchema"] = dict(schema)
        return self

    def output_schema(
        self, schema: Mapping[str, JSONValue]
    ) -> FunctionBuilder[JSONResultT, BytesResultT, StreamResultT]:
        self._values["outputSchema"] = dict(schema)
        return self

    def dependencies(
        self, dependencies: list[str]
    ) -> FunctionBuilder[JSONResultT, BytesResultT, StreamResultT]:
        self._values["dependencies"] = cast(JSONValue, dependencies)
        return self

    def env_vars(
        self, env_vars: Mapping[str, str]
    ) -> FunctionBuilder[JSONResultT, BytesResultT, StreamResultT]:
        self._values["envVars"] = dict(env_vars)
        return self

    def secrets(
        self, secrets: list[str]
    ) -> FunctionBuilder[JSONResultT, BytesResultT, StreamResultT]:
        self._values["secrets"] = cast(JSONValue, secrets)
        return self

    def memory(
        self, memory: int
    ) -> FunctionBuilder[JSONResultT, BytesResultT, StreamResultT]:
        self._values["memory"] = memory
        return self

    def timeout(
        self, timeout: int
    ) -> FunctionBuilder[JSONResultT, BytesResultT, StreamResultT]:
        self._values["timeout"] = timeout
        return self

    def permissions(
        self, permissions: FunctionPermission | Mapping[str, JSONValue]
    ) -> FunctionBuilder[JSONResultT, BytesResultT, StreamResultT]:
        self._values["permissions"] = (
            cast(
                JSONValue,
                permissions.model_dump(mode="json", by_alias=True, exclude_none=True),
            )
            if isinstance(permissions, FunctionPermission)
            else dict(permissions)
        )
        return self

    def to_definition(self) -> FunctionDefinition:
        """Validate and return the function definition."""
        return FunctionDefinition.model_validate(self._values)

    def create(self) -> JSONResultT:
        """Validate and create the function on the configured client."""
        return self._functions.create(self.to_definition())


class FunctionAccessor(Generic[JSONResultT, BytesResultT, StreamResultT]):
    """Convenience methods for a function selected by ID."""

    def __init__(
        self,
        functions: Functions[JSONResultT, BytesResultT, StreamResultT],
        function_id: str,
    ) -> None:
        self._functions = functions
        self.id = function_id

    def get(self) -> JSONResultT:
        return self._functions.get(self.id)

    def update(
        self, definition: FunctionDefinition | Mapping[str, JSONValue]
    ) -> JSONResultT:
        return self._functions.update(self.id, definition)

    def delete(self) -> JSONResultT:
        return self._functions.delete(self.id)


__all__ = [
    "FunctionAccessor",
    "FunctionBuilder",
    "FunctionDeployments",
    "FunctionExecutions",
    "FunctionVersions",
    "Functions",
]

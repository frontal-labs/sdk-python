"""Typed API resource for the ai endpoints."""

from __future__ import annotations

import inspect
import json
import time
from collections.abc import (
    AsyncIterator,
    Awaitable,
    Callable,
    Coroutine,
    Iterator,
    Mapping,
    Sequence,
)
from dataclasses import dataclass, field
from typing import Any, Generic, Literal, TypeVar, cast

import anyio
from pydantic import BaseModel, TypeAdapter
from pydantic import ValidationError as PydanticValidationError

from frontal_sdk.core.errors import FrontalError
from frontal_sdk.core.operation import Operation
from frontal_sdk.models import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatMessage,
    DonePart,
    EmbeddingsRequest,
    EmbeddingsResponse,
    EmbedResult,
    EmbedUsage,
    FinishPart,
    GenerateImageOptions,
    GenerateImageResult,
    GenerateObjectResult,
    GenerateSpeechOptions,
    GenerateTextOptions,
    GenerateTextResult,
    GenerateVideoOptions,
    GenerateVideoResult,
    JSONValue,
    Message,
    ModerationOptions,
    ModerationResult,
    MultipartPart,
    Prompt,
    PromptChain,
    QueryParams,
    RegisteredTool,
    RequestBody,
    RerankOptions,
    RerankResult,
    StreamErrorPart,
    StreamTextOptions,
    TextPart,
    TextStreamPart,
    TokenUsage,
    ToolCall,
    ToolCallPart,
    ToolDefinition,
    ToolLoopStep,
    ToolResult,
    TranscriptionOptions,
    TranscriptionResult,
    VariableDefinition,
)
from frontal_sdk.models.http import ServerEvent
from frontal_sdk.resources._base import (
    APIResource,
    BytesResultT,
    HTTPTransport,
    JSONResultT,
    StreamResultT,
)

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


class AI(
    APIResource[JSONResultT, BytesResultT, StreamResultT],
    Generic[JSONResultT, BytesResultT, StreamResultT],
):
    """Methods for the ai API endpoints."""

    def __init__(
        self, http: HTTPTransport[JSONResultT, BytesResultT, StreamResultT]
    ) -> None:
        super().__init__(http)
        self._prompts: dict[str, Prompt] = {}
        self._current_step = 0
        self._tools: dict[str, RegisteredTool[Any, Any]] = {}

    def health(self) -> JSONResultT:
        """Check the AI gateway health."""
        return self.get_health()

    def define_tool(
        self,
        name: str,
        *,
        description: str,
        parameters: type[InputT] | TypeAdapter[InputT] | dict[str, JSONValue],
        execute: Callable[[InputT], OutputT],
    ) -> RegisteredTool[InputT, OutputT]:
        """Define a named tool for the deprecated in-memory registry.

        Prefer :func:`tool` and pass the tool in ``generate_text`` or
        ``stream_text`` options.
        """
        return RegisteredTool(
            name=name,
            description=description,
            parameters=parameters,
            execute=execute,
        )

    def register_tool(self, registered: RegisteredTool[Any, Any]) -> None:
        """Register a tool for later use with :meth:`execute_tool`."""
        self._tools[registered.name] = registered

    def get_tools(self) -> list[RegisteredTool[Any, Any]]:
        """Return the process-local compatibility tool registry."""
        return list(self._tools.values())

    def _registered_tool(self, name: str) -> RegisteredTool[Any, Any]:
        try:
            return self._tools[name]
        except KeyError as error:
            raise ValueError(f"Tool not found: {name}") from error

    def execute_tool(self, name: str, params: object) -> object:
        """Execute a registered synchronous tool after validating its input."""
        registered = self._registered_tool(name)
        definition = ToolDefinition(
            description=registered.description,
            parameters=registered.parameters,
            execute=registered.execute,
        )
        result = registered.execute(_tool_input(definition, cast(JSONValue, params)))
        if inspect.isawaitable(result):
            if inspect.iscoroutine(result):
                result.close()
            raise TypeError(
                "async registered tools require AsyncFrontal.ai.execute_tool()"
            )
        return result

    def get_health(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /health."""
        return self._request(
            Operation("GET", "/health"),
            path_params=(),
            query=query,
        )

    def get_internal_models(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /internal/models."""
        return self._request(
            Operation("GET", "/internal/models"),
            path_params=(),
            query=query,
        )

    def get_internal_models_defaults(
        self, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /internal/models/defaults."""
        return self._request(
            Operation("GET", "/internal/models/defaults"),
            path_params=(),
            query=query,
        )

    def post_ai_chat_completions(
        self, *, query: QueryParams | None = None, body: RequestBody = None
    ) -> JSONResultT:
        """Call POST /ai/chat/completions."""
        return self._request(
            Operation("POST", "/ai/chat/completions"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_internal_embeddings(
        self, *, query: QueryParams | None = None, body: RequestBody = None
    ) -> JSONResultT:
        """Call POST /internal/embeddings."""
        return self._request(
            Operation("POST", "/internal/embeddings"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_internal_predictions(
        self, *, query: QueryParams | None = None, body: RequestBody = None
    ) -> JSONResultT:
        """Call POST /internal/predictions."""
        return self._request(
            Operation("POST", "/internal/predictions"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_internal_rerank(
        self, *, query: QueryParams | None = None, body: RequestBody = None
    ) -> JSONResultT:
        """Call POST /internal/rerank."""
        return self._request(
            Operation("POST", "/internal/rerank"),
            path_params=(),
            query=query,
            body=body,
        )

    def upload_internal_predictions(
        self, parts: Sequence[MultipartPart], *, fields: Mapping[str, str] | None = None
    ) -> JSONResultT:
        """Call POSTFORMDATA /internal/predictions."""
        return self._upload(
            Operation("POSTFORMDATA", "/internal/predictions"),
            parts,
            path_params=(),
            fields=fields,
        )

    def post_raw_internal_predictions(
        self, data: bytes, content_type: str, *, query: QueryParams | None = None
    ) -> BytesResultT:
        """Call POSTRAW /internal/predictions."""
        return self._post_raw(
            Operation("POSTRAW", "/internal/predictions"),
            data,
            content_type,
            path_params=(),
            query=query,
        )

    def create_prompt(
        self,
        *,
        name: str,
        template: str,
        variables: Mapping[str, VariableDefinition | Mapping[str, JSONValue]],
        metadata: Mapping[str, JSONValue] | None = None,
    ) -> Prompt:
        """Create a process-local prompt template."""
        prompt = Prompt(
            name=name,
            template=template,
            variables={
                key: value
                if isinstance(value, VariableDefinition)
                else VariableDefinition.model_validate(value)
                for key, value in variables.items()
            },
            metadata=None if metadata is None else dict(metadata),
            version="1.0.0",
        )
        self._prompts[name] = prompt
        return prompt

    def get_prompt(self, name: str, version: str | None = None) -> Prompt:
        """Get a process-local prompt template."""
        try:
            prompt = self._prompts[name]
        except KeyError as error:
            raise ValueError(f"Prompt not found: {name}") from error
        if version is not None and prompt.version != version:
            raise ValueError(
                f"Prompt {name!r} has version {prompt.version!r}, not {version!r}"
            )
        return prompt

    def update_prompt(self, name: str, updates: Mapping[str, JSONValue]) -> Prompt:
        prompt = self.get_prompt(name)
        values = prompt.model_dump(mode="python", by_alias=False)
        values.update(updates)
        updated = Prompt.model_validate(values)
        self._prompts[name] = updated
        return updated

    def chain_prompts(self, *prompts: Prompt) -> PromptChain:
        return PromptChain(prompts=list(prompts))

    def step_count_is(self, count: int) -> None:
        if count < 0:
            raise ValueError("step count must be non-negative")
        self._current_step = count

    def get_current_step(self) -> int:
        return self._current_step

    def reset_steps(self) -> None:
        self._current_step = 0


def _options(
    options: GenerateTextOptions | Mapping[str, object],
) -> GenerateTextOptions:
    if isinstance(options, GenerateTextOptions):
        return options
    return GenerateTextOptions.model_validate(options)


def _chat_request(
    options: GenerateTextOptions,
    *,
    messages: list[ChatMessage] | None = None,
    stream: bool = False,
) -> ChatCompletionRequest:
    if messages is None:
        source: list[Message]
        if options.messages is not None:
            source = options.messages
        elif isinstance(options.prompt, str):
            source = [Message(role="user", content=options.prompt)]
        else:
            source = options.prompt
        messages = [
            ChatMessage.model_validate(message.model_dump()) for message in source
        ]
    tool_choice = options.tool_choice
    if isinstance(tool_choice, dict) and isinstance(tool_choice.get("toolName"), str):
        tool_choice = {
            "type": "function",
            "function": {"name": tool_choice["toolName"]},
        }
    return ChatCompletionRequest(
        model=options.model,
        messages=messages,
        temperature=options.temperature,
        topP=options.top_p,
        frequencyPenalty=options.frequency_penalty,
        presencePenalty=options.presence_penalty,
        stop=options.stop_sequences,
        maxTokens=options.max_tokens,
        tools=_tools_for_request(options.tools),
        toolChoice=tool_choice,
        stream=stream or None,
    )


def _tools_for_request(
    tools: Mapping[str, ToolDefinition[Any, Any]] | None,
) -> list[JSONValue] | None:
    if not tools:
        return None
    result: list[JSONValue] = []
    for name, definition in tools.items():
        parameters = definition.parameters
        schema: JSONValue
        if isinstance(parameters, TypeAdapter):
            schema = cast(JSONValue, parameters.json_schema())
        elif isinstance(parameters, type) and issubclass(parameters, BaseModel):
            schema = cast(JSONValue, parameters.model_json_schema())
        else:
            schema = cast(JSONValue, parameters)
        result.append(
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": definition.description,
                    "parameters": schema,
                },
            }
        )
    return result


def _generate_text_result(response: ChatCompletionResponse) -> GenerateTextResult:
    choice = response.choices[0] if response.choices else None
    parsed_calls: list[ToolCall] = []
    if choice is not None and choice.message.tool_calls:
        for item in choice.message.tool_calls:
            if not isinstance(item, dict):
                continue
            function = item.get("function")
            if not isinstance(function, dict):
                continue
            name = function.get("name")
            if not isinstance(name, str):
                name = ""
            raw_arguments = function.get("arguments")
            input_value: JSONValue = {}
            if isinstance(raw_arguments, str):
                try:
                    import json

                    input_value = cast(JSONValue, json.loads(raw_arguments))
                except ValueError:
                    input_value = raw_arguments
            elif raw_arguments is not None:
                input_value = cast(JSONValue, raw_arguments)
            call_id = item.get("id")
            parsed_calls.append(
                ToolCall(
                    id=call_id if isinstance(call_id, str) else None,
                    toolName=name,
                    input=input_value,
                )
            )

    raw_reason = choice.finish_reason if choice is not None else None
    finish_reason: Literal[
        "stop", "length", "content-filter", "tool-calls", "error", "other"
    ]
    if raw_reason == "tool_calls" or (parsed_calls and not raw_reason):
        finish_reason = "tool-calls"
    elif raw_reason in {"stop", "length", "content-filter", "error", "other"}:
        finish_reason = cast(
            Literal["stop", "length", "content-filter", "tool-calls", "error", "other"],
            raw_reason,
        )
    else:
        finish_reason = "other"
    usage = response.usage or TokenUsage(
        prompt_tokens=0, completion_tokens=0, total_tokens=0
    )
    text = choice.message.content or "" if choice is not None else ""
    step = ToolLoopStep(
        step=1,
        text=text,
        finishReason=finish_reason,
        toolCalls=parsed_calls,
        toolResults=[],
        usage=usage,
    )
    return GenerateTextResult(
        text=text,
        finishReason=finish_reason,
        usage=usage,
        toolCalls=parsed_calls,
        toolResults=[],
        steps=[step],
    )


def _schema_json(
    schema: type[BaseModel] | TypeAdapter[Any] | Mapping[str, JSONValue],
) -> JSONValue:
    if isinstance(schema, TypeAdapter):
        return cast(JSONValue, schema.json_schema())
    if isinstance(schema, type) and issubclass(schema, BaseModel):
        return cast(JSONValue, schema.model_json_schema())
    return cast(JSONValue, dict(schema))


def _validate_object(
    schema: type[BaseModel] | TypeAdapter[Any] | Mapping[str, JSONValue],
    value: object,
) -> Any:
    if isinstance(schema, TypeAdapter):
        return schema.validate_python(value)
    if isinstance(schema, type) and issubclass(schema, BaseModel):
        return schema.model_validate(value)
    return cast(JSONValue, value)


def _response_usage(usage: TokenUsage | None) -> TokenUsage:
    return usage or TokenUsage(prompt_tokens=0, completion_tokens=0, total_tokens=0)


def _image_result(value: JSONValue) -> GenerateImageResult:
    data = value.get("data") if isinstance(value, dict) else None
    if isinstance(data, list):
        return GenerateImageResult.model_validate(
            {
                "images": [
                    {
                        "url": item.get("url"),
                        "b64Json": item.get("b64Json", item.get("b64_json")),
                    }
                    for item in data
                    if isinstance(item, dict)
                ]
            }
        )
    return GenerateImageResult.model_validate(value)


def _object_request(
    model: str,
    prompt: str,
    schema: type[BaseModel] | TypeAdapter[Any] | Mapping[str, JSONValue],
    temperature: float | None,
) -> JSONValue:
    instruction = (
        "You are a helpful assistant designed to output JSON. The JSON must "
        "strictly follow this schema description: "
        f"{json.dumps(_schema_json(schema))}"
    )
    request = ChatCompletionRequest(
        model=model,
        messages=[
            ChatMessage(role="system", content=instruction),
            ChatMessage(role="user", content=prompt),
        ],
        temperature=temperature,
        responseFormat={"type": "json_object"},
    )
    return cast(
        JSONValue, request.model_dump(mode="json", by_alias=True, exclude_none=True)
    )


def _rerank_request(options: RerankOptions) -> JSONValue:
    documents: list[JSONValue] = []
    for item in options.documents:
        if isinstance(item, str):
            documents.append({"content": item})
        else:
            documents.append(
                cast(
                    JSONValue,
                    item.model_dump(mode="json", by_alias=True, exclude_none=True),
                )
            )
    body: dict[str, JSONValue] = {
        "model": options.model,
        "query": options.query,
        "documents": documents,
    }
    if options.top_k is not None:
        body["topK"] = options.top_k
    if options.criteria is not None:
        body["criteria"] = options.criteria
    return body


def _tool_input(definition: ToolDefinition[Any, Any], value: JSONValue) -> object:
    parameters = definition.parameters
    if isinstance(parameters, TypeAdapter):
        return parameters.validate_python(value)
    if isinstance(parameters, type) and issubclass(parameters, BaseModel):
        return parameters.model_validate(value)
    return value


def _json_value(value: object) -> JSONValue:
    if isinstance(value, BaseModel):
        value = value.model_dump(mode="json", by_alias=True, exclude_none=True)
    return cast(JSONValue, json.loads(json.dumps(value)))


def _tool_messages(
    calls: list[ToolCall], results: list[ToolResult], text: str
) -> list[ChatMessage]:
    result_by_id = {item.id: item for item in results}
    messages: list[ChatMessage] = [
        ChatMessage(
            role="assistant",
            content=text or None,
            tool_calls=[
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.tool_name,
                        "arguments": json.dumps(call.input),
                    },
                }
                for call in calls
            ],
        )
    ]
    for call in calls:
        result = result_by_id.get(call.id)
        if result is None:
            continue
        content: JSONValue = {"error": result.error} if result.error else result.output
        messages.append(
            ChatMessage(
                role="tool",
                tool_call_id=call.id,
                name=call.tool_name,
                content=json.dumps(content),
            )
        )
    return messages


def _combined_usage(current: TokenUsage, previous: TokenUsage) -> TokenUsage:
    return TokenUsage(
        prompt_tokens=current.prompt_tokens + previous.prompt_tokens,
        completion_tokens=current.completion_tokens + previous.completion_tokens,
        total_tokens=current.total_tokens + previous.total_tokens,
    )


@dataclass
class _PendingToolCall:
    id: str | None = None
    name: str = ""
    arguments: str = ""


@dataclass
class _StreamState:
    options: StreamTextOptions
    usage: TokenUsage = field(
        default_factory=lambda: TokenUsage(
            prompt_tokens=0, completion_tokens=0, total_tokens=0
        )
    )
    finish_reason: str | None = None
    pending_tools: dict[int, _PendingToolCall] = field(default_factory=dict)
    id_indexes: dict[str, int] = field(default_factory=dict)
    emitted: bool = False


def _stream_event_parts(
    event: ServerEvent, state: _StreamState
) -> list[TextStreamPart]:
    value = event.data
    if value == "[DONE]" or not isinstance(value, dict):
        return []
    state.emitted = True
    usage = value.get("usage")
    if isinstance(usage, dict):
        state.usage = TokenUsage(
            prompt_tokens=_int_field(usage, "promptTokens", "prompt_tokens"),
            completion_tokens=_int_field(
                usage, "completionTokens", "completion_tokens"
            ),
            total_tokens=_int_field(usage, "totalTokens", "total_tokens"),
        )
    choices = value.get("choices")
    if not isinstance(choices, list) or not choices or not isinstance(choices[0], dict):
        return []
    choice = choices[0]
    delta = choice.get("delta")
    parts: list[TextStreamPart] = []
    if isinstance(delta, dict):
        content = delta.get("content")
        if isinstance(content, str) and content:
            if state.options.on_chunk is not None:
                state.options.on_chunk(content)
            parts.append(TextPart(type="text", text=content))
        calls = delta.get("toolCalls", delta.get("tool_calls"))
        if isinstance(calls, list):
            for call in calls:
                if not isinstance(call, dict):
                    continue
                call_id = call.get("id")
                index = call.get("index")
                if isinstance(index, int):
                    call_index = index
                elif isinstance(call_id, str):
                    call_index = state.id_indexes.get(call_id, len(state.pending_tools))
                else:
                    call_index = len(state.pending_tools)
                pending = state.pending_tools.setdefault(call_index, _PendingToolCall())
                if isinstance(call_id, str):
                    pending.id = call_id
                    state.id_indexes[call_id] = call_index
                function = call.get("function")
                if isinstance(function, dict):
                    name = function.get("name")
                    arguments = function.get("arguments")
                    if isinstance(name, str) and name:
                        pending.name = name
                    if isinstance(arguments, str):
                        pending.arguments += arguments
    reason = choice.get("finishReason", choice.get("finish_reason"))
    if isinstance(reason, str):
        state.finish_reason = reason
    return parts


def _int_field(value: Mapping[str, object], *names: str) -> int:
    for name in names:
        result = value.get(name)
        if isinstance(result, int) and not isinstance(result, bool):
            return result
    return 0


def _stream_finish_parts(state: _StreamState) -> list[TextStreamPart]:
    parts: list[TextStreamPart] = []
    for _, pending in sorted(state.pending_tools.items()):
        try:
            input_value: JSONValue = (
                json.loads(pending.arguments) if pending.arguments else {}
            )
        except ValueError:
            input_value = pending.arguments
        parts.append(
            ToolCallPart(
                type="tool-call",
                id=pending.id,
                toolName=pending.name,
                input=input_value,
            )
        )
    if state.emitted:
        reason = _finish_reason(state.finish_reason)
        if reason == "other" and state.pending_tools:
            reason = "tool-calls"
        parts.append(FinishPart(type="finish", finishReason=reason, usage=state.usage))
    parts.append(DonePart(type="done"))
    return parts


def _finish_reason(
    reason: str | None,
) -> Literal["stop", "length", "content-filter", "tool-calls", "error", "other"]:
    if reason in {"stop", "length", "error", "other"}:
        return cast(Literal["stop", "length", "error", "other"], reason)
    if reason in {"tool_calls", "tool-calls"}:
        return "tool-calls"
    if reason in {"content_filter", "content-filter"}:
        return "content-filter"
    return "other"


def _stream_options(
    options: StreamTextOptions | Mapping[str, object],
) -> StreamTextOptions:
    if isinstance(options, StreamTextOptions):
        return options
    if isinstance(options, GenerateTextOptions):
        return StreamTextOptions.model_validate(
            options.model_dump(mode="python", by_alias=True, exclude_none=True)
        )
    return StreamTextOptions.model_validate(options)


def _stream_body(options: StreamTextOptions) -> JSONValue:
    request = _chat_request(options, stream=True)
    return cast(
        JSONValue, request.model_dump(mode="json", by_alias=True, exclude_none=True)
    )


class SyncAI(AI[JSONValue, bytes, Iterator[ServerEvent]]):
    """Synchronous high-level AI helpers plus every raw AI endpoint."""

    def stream_text(
        self, options: StreamTextOptions | Mapping[str, object]
    ) -> Iterator[TextStreamPart]:
        """Stream chat text and tool-call parts from the AI gateway."""
        validated = _stream_options(options)
        body = _stream_body(validated)

        def parts() -> Iterator[TextStreamPart]:
            state = _StreamState(validated)
            try:
                events = self._stream_request(
                    Operation("POST", "/ai/chat/completions"),
                    body=body,
                    max_retries=validated.stream_retries,
                )
                for event in events:
                    yield from _stream_event_parts(event, state)
                yield from _stream_finish_parts(state)
            except FrontalError as error:
                if validated.on_error is not None:
                    validated.on_error(str(error))
                yield StreamErrorPart(type="error", error=str(error))
                yield DonePart(type="done")
            except BaseException:
                if validated.on_abort is not None:
                    validated.on_abort()
                raise

        return parts()

    def generate_text(
        self, options: GenerateTextOptions | Mapping[str, object]
    ) -> GenerateTextResult:
        """Generate text and return a validated, normalized Pydantic result."""
        validated = _options(options)
        messages = _chat_request(validated).messages
        steps: list[ToolLoopStep] = []
        total_usage = TokenUsage(prompt_tokens=0, completion_tokens=0, total_tokens=0)
        latest: GenerateTextResult | None = None
        max_steps = validated.max_steps if validated.tools else 1
        for step_number in range(1, max_steps + 1):
            request = _chat_request(validated, messages=messages)
            body = cast(
                JSONValue,
                request.model_dump(mode="json", by_alias=True, exclude_none=True),
            )
            response = ChatCompletionResponse.model_validate(
                self.post_ai_chat_completions(body=body)
            )
            result = _generate_text_result(response)
            total_usage = _combined_usage(total_usage, result.usage)
            calls = result.tool_calls
            tool_results: list[ToolResult] = []
            all_calls_ran = bool(calls)
            for call in calls:
                definition = (validated.tools or {}).get(call.tool_name)
                if definition is None:
                    all_calls_ran = False
                    continue
                try:
                    parameters = _tool_input(definition, call.input)
                    output = definition.execute(parameters)
                    if inspect.isawaitable(output):
                        raise TypeError(
                            "sync generate_text requires synchronous tool executors"
                        )
                    tool_results.append(
                        ToolResult(
                            id=call.id,
                            toolName=call.tool_name,
                            input=_json_value(parameters),
                            output=_json_value(output),
                        )
                    )
                except Exception as error:
                    tool_results.append(
                        ToolResult(
                            id=call.id,
                            toolName=call.tool_name,
                            input=call.input,
                            error=str(error),
                        )
                    )
            base_step = result.steps[0]
            finished_step = base_step.model_copy(
                update={"step": step_number, "tool_results": tool_results}
            )
            steps.append(finished_step)
            if validated.on_step_finish is not None:
                validated.on_step_finish(finished_step)
            latest = result.model_copy(
                update={
                    "tool_results": tool_results,
                    "steps": list(steps),
                    "usage": total_usage,
                }
            )
            if (
                result.finish_reason != "tool-calls"
                or not calls
                or not all_calls_ran
                or step_number == max_steps
            ):
                break
            messages.extend(_tool_messages(calls, tool_results, result.text))
        if latest is None:
            raise ValueError("generate_text executed no model calls")
        return latest

    def embed(self, model: str, input: str | list[str]) -> EmbedResult:
        """Create text embeddings and normalize the vector response."""
        request = EmbeddingsRequest(model=model, input=input)
        body = cast(JSONValue, request.model_dump(mode="json", by_alias=True))
        response = EmbeddingsResponse.model_validate(
            self.post_internal_embeddings(body=body)
        )
        return EmbedResult(
            embeddings=[item.embedding for item in response.data],
            usage=EmbedUsage(totalTokens=response.usage.total_tokens),
        )

    def list_models(self) -> list[str]:
        """List model IDs advertised by the AI gateway."""
        response = self.get_internal_models()
        if isinstance(response, dict):
            data = response.get("data")
            if isinstance(data, list) and data:
                if isinstance(data[0], dict) and isinstance(data[0].get("id"), str):
                    return [
                        cast(str, item["id"])
                        for item in data
                        if isinstance(item, dict) and isinstance(item.get("id"), str)
                    ]
        if isinstance(response, list) and all(
            isinstance(item, str) for item in response
        ):
            return cast(list[str], response)
        return []

    def get_default_models(self) -> dict[str, str]:
        """Return the gateway's model ID for each supported capability."""
        response = self.get_internal_models_defaults()
        if isinstance(response, dict):
            return {
                key: value for key, value in response.items() if isinstance(value, str)
            }
        return {}

    def count_tokens(self, text: str) -> int:
        """Estimate tokens with the same four-characters-per-token heuristic."""
        return (len(text) + 3) // 4

    def estimate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Estimate cost using the SDK's documented placeholder rates."""
        input_rate, output_rate = (
            (0.000001, 0.000002) if model == "frontal-ai-fast" else (0.00001, 0.00003)
        )
        return input_tokens * input_rate + output_tokens * output_rate

    def generate_object(
        self,
        *,
        model: str,
        prompt: str,
        schema: type[BaseModel] | TypeAdapter[Any] | Mapping[str, JSONValue],
        temperature: float | None = None,
        max_retries: int = 0,
    ) -> GenerateObjectResult[Any]:
        """Generate JSON and validate it with a Pydantic model or adapter."""
        if max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        body = _object_request(model, prompt, schema, temperature)
        last_error: Exception | None = None
        for attempt in range(max_retries + 1):
            if attempt:
                time.sleep(0.5)
            try:
                response = ChatCompletionResponse.model_validate(
                    self.post_ai_chat_completions(body=body)
                )
                content = (
                    response.choices[0].message.content if response.choices else None
                )
                if not content:
                    raise ValueError("No content generated")
                value = _validate_object(schema, json.loads(content))
                return GenerateObjectResult[Any](
                    object=value,
                    usage=_response_usage(response.usage),
                )
            except FrontalError as error:
                if not error.retryable:
                    raise
                last_error = error
            except (ValueError, PydanticValidationError) as error:
                last_error = error
        raise last_error or ValueError("generate_object failed after retries")

    def generate_speech(
        self, options: GenerateSpeechOptions | Mapping[str, JSONValue]
    ) -> bytes:
        """Generate speech and return the raw audio bytes."""
        values = (
            options
            if isinstance(options, GenerateSpeechOptions)
            else GenerateSpeechOptions.model_validate(options)
        )
        body: dict[str, JSONValue] = {
            "model": values.model or "tts-1",
            "input": values.text,
            "voice": values.voice,
        }
        if values.speed is not None:
            body["speed"] = values.speed
        if values.format is not None:
            body["responseFormat"] = values.format
        return self.post_raw_internal_predictions(
            json.dumps(body, separators=(",", ":")).encode(), "application/json"
        )

    def generate_image(
        self, options: GenerateImageOptions | Mapping[str, JSONValue]
    ) -> GenerateImageResult:
        values = (
            options
            if isinstance(options, GenerateImageOptions)
            else GenerateImageOptions.model_validate(options)
        )
        body: dict[str, JSONValue] = {
            "prompt": values.prompt,
            "model": values.model or "dall-e-3",
            "n": values.n or 1,
            "size": values.size or "1024x1024",
            "responseFormat": "url",
        }
        if values.quality is not None:
            body["quality"] = values.quality
        if values.style is not None:
            body["style"] = values.style
        return _image_result(self.post_internal_predictions(body=body))

    def generate_video(
        self, options: GenerateVideoOptions | Mapping[str, JSONValue]
    ) -> GenerateVideoResult:
        values = (
            options
            if isinstance(options, GenerateVideoOptions)
            else GenerateVideoOptions.model_validate(options)
        )
        body = cast(
            JSONValue,
            values.model_dump(mode="json", by_alias=True, exclude_none=True),
        )
        return GenerateVideoResult.model_validate(
            self.post_internal_predictions(body=body)
        )

    def transcribe(
        self, options: TranscriptionOptions | Mapping[str, object]
    ) -> TranscriptionResult:
        values = (
            options
            if isinstance(options, TranscriptionOptions)
            else TranscriptionOptions.model_validate(options)
        )
        fields = {"model": values.model}
        for key, value in (
            ("language", values.language),
            ("prompt", values.prompt),
            ("response_format", values.response_format),
        ):
            if value is not None:
                fields[key] = value
        if values.temperature is not None:
            fields["temperature"] = str(values.temperature)
        response = self.upload_internal_predictions(
            [MultipartPart("file", values.file, values.filename, values.content_type)],
            fields=fields,
        )
        return TranscriptionResult.model_validate(response)

    def moderate(
        self, options: ModerationOptions | Mapping[str, JSONValue]
    ) -> ModerationResult:
        values = (
            options
            if isinstance(options, ModerationOptions)
            else ModerationOptions.model_validate(options)
        )
        body: dict[str, JSONValue] = {
            "input": cast(JSONValue, values.input),
            "model": values.model or "text-moderation-latest",
        }
        return ModerationResult.model_validate(
            self.post_internal_predictions(body=body)
        )

    def rerank(self, options: RerankOptions | Mapping[str, JSONValue]) -> RerankResult:
        values = (
            options
            if isinstance(options, RerankOptions)
            else RerankOptions.model_validate(options)
        )
        return RerankResult.model_validate(
            self.post_internal_rerank(body=_rerank_request(values))
        )


class AsyncAI(
    AI[
        Coroutine[Any, Any, JSONValue],
        Coroutine[Any, Any, bytes],
        AsyncIterator[ServerEvent],
    ]
):
    """Asynchronous high-level AI helpers plus every raw AI endpoint."""

    async def execute_tool(self, name: str, params: object) -> object:
        """Execute a registered tool, awaiting its result when needed."""
        registered = self._registered_tool(name)
        definition = ToolDefinition(
            description=registered.description,
            parameters=registered.parameters,
            execute=registered.execute,
        )
        result = registered.execute(_tool_input(definition, cast(JSONValue, params)))
        if inspect.isawaitable(result):
            return await result
        return result

    async def stream_text(
        self, options: StreamTextOptions | Mapping[str, object]
    ) -> AsyncIterator[TextStreamPart]:
        """Asynchronously stream chat text and tool-call parts."""
        validated = _stream_options(options)
        body = _stream_body(validated)
        state = _StreamState(validated)
        try:
            events = self._stream_request(
                Operation("POST", "/ai/chat/completions"),
                body=body,
                max_retries=validated.stream_retries,
            )
            async for event in events:
                for part in _stream_event_parts(event, state):
                    yield part
            for part in _stream_finish_parts(state):
                yield part
        except FrontalError as error:
            if validated.on_error is not None:
                validated.on_error(str(error))
            yield StreamErrorPart(type="error", error=str(error))
            yield DonePart(type="done")
        except BaseException:
            if validated.on_abort is not None:
                validated.on_abort()
            raise

    async def generate_text(
        self, options: GenerateTextOptions | Mapping[str, object]
    ) -> GenerateTextResult:
        """Generate text and return a validated, normalized Pydantic result."""
        validated = _options(options)
        messages = _chat_request(validated).messages
        steps: list[ToolLoopStep] = []
        total_usage = TokenUsage(prompt_tokens=0, completion_tokens=0, total_tokens=0)
        latest: GenerateTextResult | None = None
        max_steps = validated.max_steps if validated.tools else 1
        for step_number in range(1, max_steps + 1):
            request = _chat_request(validated, messages=messages)
            body = cast(
                JSONValue,
                request.model_dump(mode="json", by_alias=True, exclude_none=True),
            )
            response = ChatCompletionResponse.model_validate(
                await self.post_ai_chat_completions(body=body)
            )
            result = _generate_text_result(response)
            total_usage = _combined_usage(total_usage, result.usage)
            calls = result.tool_calls
            tool_results: list[ToolResult] = []
            all_calls_ran = bool(calls)
            for call in calls:
                definition = (validated.tools or {}).get(call.tool_name)
                if definition is None:
                    all_calls_ran = False
                    continue
                try:
                    parameters = _tool_input(definition, call.input)
                    output = definition.execute(parameters)
                    if inspect.isawaitable(output):
                        output = await cast(Awaitable[object], output)
                    tool_results.append(
                        ToolResult(
                            id=call.id,
                            toolName=call.tool_name,
                            input=_json_value(parameters),
                            output=_json_value(output),
                        )
                    )
                except Exception as error:
                    tool_results.append(
                        ToolResult(
                            id=call.id,
                            toolName=call.tool_name,
                            input=call.input,
                            error=str(error),
                        )
                    )
            base_step = result.steps[0]
            finished_step = base_step.model_copy(
                update={"step": step_number, "tool_results": tool_results}
            )
            steps.append(finished_step)
            if validated.on_step_finish is not None:
                validated.on_step_finish(finished_step)
            latest = result.model_copy(
                update={
                    "tool_results": tool_results,
                    "steps": list(steps),
                    "usage": total_usage,
                }
            )
            if (
                result.finish_reason != "tool-calls"
                or not calls
                or not all_calls_ran
                or step_number == max_steps
            ):
                break
            messages.extend(_tool_messages(calls, tool_results, result.text))
        if latest is None:
            raise ValueError("generate_text executed no model calls")
        return latest

    async def embed(self, model: str, input: str | list[str]) -> EmbedResult:
        """Create text embeddings and normalize the vector response."""
        request = EmbeddingsRequest(model=model, input=input)
        body = cast(JSONValue, request.model_dump(mode="json", by_alias=True))
        response = EmbeddingsResponse.model_validate(
            await self.post_internal_embeddings(body=body)
        )
        return EmbedResult(
            embeddings=[item.embedding for item in response.data],
            usage=EmbedUsage(totalTokens=response.usage.total_tokens),
        )

    async def list_models(self) -> list[str]:
        """List model IDs advertised by the AI gateway."""
        response = await self.get_internal_models()
        if isinstance(response, dict):
            data = response.get("data")
            if isinstance(data, list) and data:
                if isinstance(data[0], dict) and isinstance(data[0].get("id"), str):
                    return [
                        cast(str, item["id"])
                        for item in data
                        if isinstance(item, dict) and isinstance(item.get("id"), str)
                    ]
        if isinstance(response, list) and all(
            isinstance(item, str) for item in response
        ):
            return cast(list[str], response)
        return []

    async def get_default_models(self) -> dict[str, str]:
        """Return the gateway's model ID for each supported capability."""
        response = await self.get_internal_models_defaults()
        if isinstance(response, dict):
            return {
                key: value for key, value in response.items() if isinstance(value, str)
            }
        return {}

    def count_tokens(self, text: str) -> int:
        """Estimate tokens with the same four-characters-per-token heuristic."""
        return (len(text) + 3) // 4

    def estimate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Estimate cost using the SDK's documented placeholder rates."""
        input_rate, output_rate = (
            (0.000001, 0.000002) if model == "frontal-ai-fast" else (0.00001, 0.00003)
        )
        return input_tokens * input_rate + output_tokens * output_rate

    async def generate_object(
        self,
        *,
        model: str,
        prompt: str,
        schema: type[BaseModel] | TypeAdapter[Any] | Mapping[str, JSONValue],
        temperature: float | None = None,
        max_retries: int = 0,
    ) -> GenerateObjectResult[Any]:
        """Generate JSON and validate it with a Pydantic model or adapter."""
        if max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        body = _object_request(model, prompt, schema, temperature)
        last_error: Exception | None = None
        for attempt in range(max_retries + 1):
            if attempt:
                await anyio.sleep(0.5)
            try:
                response = ChatCompletionResponse.model_validate(
                    await self.post_ai_chat_completions(body=body)
                )
                content = (
                    response.choices[0].message.content if response.choices else None
                )
                if not content:
                    raise ValueError("No content generated")
                value = _validate_object(schema, json.loads(content))
                return GenerateObjectResult[Any](
                    object=value,
                    usage=_response_usage(response.usage),
                )
            except FrontalError as error:
                if not error.retryable:
                    raise
                last_error = error
            except (ValueError, PydanticValidationError) as error:
                last_error = error
        raise last_error or ValueError("generate_object failed after retries")

    async def generate_speech(
        self, options: GenerateSpeechOptions | Mapping[str, JSONValue]
    ) -> bytes:
        values = (
            options
            if isinstance(options, GenerateSpeechOptions)
            else GenerateSpeechOptions.model_validate(options)
        )
        body: dict[str, JSONValue] = {
            "model": values.model or "tts-1",
            "input": values.text,
            "voice": values.voice,
        }
        if values.speed is not None:
            body["speed"] = values.speed
        if values.format is not None:
            body["responseFormat"] = values.format
        return await self.post_raw_internal_predictions(
            json.dumps(body, separators=(",", ":")).encode(), "application/json"
        )

    async def generate_image(
        self, options: GenerateImageOptions | Mapping[str, JSONValue]
    ) -> GenerateImageResult:
        values = (
            options
            if isinstance(options, GenerateImageOptions)
            else GenerateImageOptions.model_validate(options)
        )
        body: dict[str, JSONValue] = {
            "prompt": values.prompt,
            "model": values.model or "dall-e-3",
            "n": values.n or 1,
            "size": values.size or "1024x1024",
            "responseFormat": "url",
        }
        if values.quality is not None:
            body["quality"] = values.quality
        if values.style is not None:
            body["style"] = values.style
        return _image_result(await self.post_internal_predictions(body=body))

    async def generate_video(
        self, options: GenerateVideoOptions | Mapping[str, JSONValue]
    ) -> GenerateVideoResult:
        values = (
            options
            if isinstance(options, GenerateVideoOptions)
            else GenerateVideoOptions.model_validate(options)
        )
        body = cast(
            JSONValue,
            values.model_dump(mode="json", by_alias=True, exclude_none=True),
        )
        response = await self.post_internal_predictions(body=body)
        return GenerateVideoResult.model_validate(response)

    async def transcribe(
        self, options: TranscriptionOptions | Mapping[str, object]
    ) -> TranscriptionResult:
        values = (
            options
            if isinstance(options, TranscriptionOptions)
            else TranscriptionOptions.model_validate(options)
        )
        fields = {"model": values.model}
        for key, value in (
            ("language", values.language),
            ("prompt", values.prompt),
            ("response_format", values.response_format),
        ):
            if value is not None:
                fields[key] = value
        if values.temperature is not None:
            fields["temperature"] = str(values.temperature)
        response = await self.upload_internal_predictions(
            [MultipartPart("file", values.file, values.filename, values.content_type)],
            fields=fields,
        )
        return TranscriptionResult.model_validate(response)

    async def moderate(
        self, options: ModerationOptions | Mapping[str, JSONValue]
    ) -> ModerationResult:
        values = (
            options
            if isinstance(options, ModerationOptions)
            else ModerationOptions.model_validate(options)
        )
        body: dict[str, JSONValue] = {
            "input": cast(JSONValue, values.input),
            "model": values.model or "text-moderation-latest",
        }
        response = await self.post_internal_predictions(body=body)
        return ModerationResult.model_validate(response)

    async def rerank(
        self, options: RerankOptions | Mapping[str, JSONValue]
    ) -> RerankResult:
        values = (
            options
            if isinstance(options, RerankOptions)
            else RerankOptions.model_validate(options)
        )
        response = await self.post_internal_rerank(body=_rerank_request(values))
        return RerankResult.model_validate(response)


def tool(
    *,
    description: str,
    parameters: type[InputT] | TypeAdapter[InputT] | dict[str, JSONValue],
    execute: Callable[[InputT], OutputT],
) -> ToolDefinition[InputT, OutputT]:
    """Define a local tool for ``generate_text`` tool calls."""
    return ToolDefinition(
        description=description,
        parameters=parameters,
        execute=execute,
    )


__all__ = ["AI", "AsyncAI", "SyncAI", "tool"]

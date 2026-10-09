"""Pydantic models for the Frontal AI service."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Annotated, Any, Generic, Literal, TypeVar, Union

from pydantic import AliasChoices, ConfigDict, Field, TypeAdapter

from frontal_sdk.models.types import APIModel, JSONValue


class AIModel(APIModel):
    """AI payload model that tolerates fields added by compatible providers."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)


class Message(AIModel):
    """A conversation message used by text generation."""

    role: Literal["system", "user", "assistant", "tool"]
    content: str


class ToolCall(AIModel):
    """A parsed model tool call."""

    id: str | None = None
    tool_name: str = Field(alias="toolName")
    input: JSONValue = None


class ToolResult(AIModel):
    """Result of running a tool requested during generation."""

    id: str | None = None
    tool_name: str = Field(alias="toolName")
    input: JSONValue = None
    output: JSONValue = None
    error: str | None = None


class TokenUsage(AIModel):
    """Token counts returned by text generation."""

    prompt_tokens: int = Field(
        validation_alias=AliasChoices("promptTokens", "prompt_tokens"),
        serialization_alias="promptTokens",
    )
    completion_tokens: int = Field(
        validation_alias=AliasChoices("completionTokens", "completion_tokens"),
        serialization_alias="completionTokens",
    )
    total_tokens: int = Field(
        validation_alias=AliasChoices("totalTokens", "total_tokens"),
        serialization_alias="totalTokens",
    )


class ToolLoopStep(AIModel):
    """One model call in a multi-step tool loop."""

    step: int
    text: str
    finish_reason: Literal[
        "stop", "length", "content-filter", "tool-calls", "error", "other"
    ] = Field(alias="finishReason")
    tool_calls: list[ToolCall] = Field(default_factory=list, alias="toolCalls")
    tool_results: list[ToolResult] = Field(default_factory=list, alias="toolResults")
    usage: TokenUsage


ToolInputT = TypeVar("ToolInputT")
ToolOutputT = TypeVar("ToolOutputT")


@dataclass(frozen=True)
class ToolDefinition(Generic[ToolInputT, ToolOutputT]):
    """A local callable exposed to a model as a JSON-schema tool."""

    description: str
    parameters: type[ToolInputT] | TypeAdapter[ToolInputT] | dict[str, JSONValue]
    execute: Callable[[ToolInputT], ToolOutputT]


class GenerateTextOptions(AIModel):
    """Validated inputs for :meth:`AI.generate_text`."""

    model_config = ConfigDict(
        extra="ignore", populate_by_name=True, arbitrary_types_allowed=True
    )

    model: str
    prompt: str | list[Message]
    messages: list[Message] | None = None
    max_tokens: int | None = Field(default=None, alias="maxTokens", ge=1)
    temperature: float | None = None
    top_p: float | None = Field(default=None, alias="topP")
    frequency_penalty: float | None = Field(default=None, alias="frequencyPenalty")
    presence_penalty: float | None = Field(default=None, alias="presencePenalty")
    stop_sequences: list[str] | None = Field(default=None, alias="stopSequences")
    tools: dict[str, ToolDefinition[Any, Any]] | None = None
    tool_choice: JSONValue = Field(default=None, alias="toolChoice")
    max_steps: int = Field(default=1, alias="maxSteps", ge=1, le=50)
    on_step_finish: Callable[[ToolLoopStep], None] | None = Field(
        default=None, alias="onStepFinish", exclude=True
    )


class StreamTextOptions(GenerateTextOptions):
    on_chunk: Callable[[str], None] | None = Field(
        default=None, alias="onChunk", exclude=True
    )
    on_error: Callable[[str], None] | None = Field(
        default=None, alias="onError", exclude=True
    )
    on_abort: Callable[[], None] | None = Field(
        default=None, alias="onAbort", exclude=True
    )
    stream_retries: int = Field(default=0, alias="streamRetries", ge=0, le=5)


class TextPart(AIModel):
    type: Literal["text"]
    text: str


class ToolCallPart(AIModel):
    type: Literal["tool-call"]
    id: str | None = None
    tool_name: str = Field(alias="toolName")
    input: JSONValue = None


class FinishPart(AIModel):
    type: Literal["finish"]
    finish_reason: Literal[
        "stop", "length", "content-filter", "tool-calls", "error", "other"
    ] = Field(alias="finishReason")
    usage: TokenUsage


class StreamErrorPart(AIModel):
    type: Literal["error"]
    error: str


class AbortPart(AIModel):
    type: Literal["abort"]


class DonePart(AIModel):
    type: Literal["done"]


TextStreamPart = Annotated[
    Union[TextPart, ToolCallPart, FinishPart, StreamErrorPart, AbortPart, DonePart],
    Field(discriminator="type"),
]


class ChatMessage(AIModel):
    """OpenAI-compatible chat completion message."""

    role: Literal["system", "user", "assistant", "function", "tool"]
    content: str | None = None
    name: str | None = None
    tool_calls: list[JSONValue] | None = Field(
        default=None,
        validation_alias=AliasChoices("toolCalls", "tool_calls"),
        serialization_alias="toolCalls",
    )
    tool_call_id: str | None = Field(
        default=None,
        validation_alias=AliasChoices("toolCallId", "tool_call_id"),
        serialization_alias="toolCallId",
    )


class ChatCompletionRequest(AIModel):
    """Wire request for the OpenAI-compatible chat completion endpoint."""

    model: str
    messages: list[ChatMessage]
    temperature: float | None = None
    top_p: float | None = Field(default=None, alias="topP")
    n: int | None = None
    stream: bool | None = None
    stop: str | list[str] | None = None
    max_tokens: int | None = Field(default=None, alias="maxTokens", ge=1)
    presence_penalty: float | None = Field(default=None, alias="presencePenalty")
    frequency_penalty: float | None = Field(default=None, alias="frequencyPenalty")
    logit_bias: dict[str, float] | None = Field(default=None, alias="logitBias")
    user: str | None = None
    response_format: dict[str, str] | None = Field(default=None, alias="responseFormat")
    seed: int | None = None
    tools: list[JSONValue] | None = None
    tool_choice: JSONValue = Field(default=None, alias="toolChoice")


class ChatCompletionChoice(AIModel):
    """One completion choice."""

    index: int
    message: ChatMessage
    finish_reason: str | None = Field(
        default=None,
        validation_alias=AliasChoices("finishReason", "finish_reason"),
        serialization_alias="finishReason",
    )


class ChatCompletionResponse(AIModel):
    """Validated OpenAI-compatible chat completion response."""

    id: str
    object: Literal["chat.completion"]
    created: int
    model: str
    choices: list[ChatCompletionChoice]
    usage: TokenUsage | None = None
    system_fingerprint: str | None = Field(
        default=None,
        validation_alias=AliasChoices("systemFingerprint", "system_fingerprint"),
        serialization_alias="systemFingerprint",
    )


class GenerateTextResult(AIModel):
    """Normalized result from :meth:`AI.generate_text`."""

    text: str
    finish_reason: Literal[
        "stop", "length", "content-filter", "tool-calls", "error", "other"
    ] = Field(alias="finishReason")
    usage: TokenUsage
    tool_calls: list[ToolCall] = Field(default_factory=list, alias="toolCalls")
    tool_results: list[ToolResult] = Field(default_factory=list, alias="toolResults")
    steps: list[ToolLoopStep] = Field(default_factory=list)


class EmbeddingsRequest(AIModel):
    """Wire request for the embeddings endpoint."""

    model: str
    input: str | list[str]


class EmbeddingItem(AIModel):
    """One vector in an embeddings response."""

    object: Literal["embedding"]
    embedding: list[float]
    index: int


class EmbeddingsUsage(AIModel):
    """Token counts for an embeddings response."""

    prompt_tokens: int = Field(
        validation_alias=AliasChoices("promptTokens", "prompt_tokens"),
        serialization_alias="promptTokens",
    )
    total_tokens: int = Field(
        validation_alias=AliasChoices("totalTokens", "total_tokens"),
        serialization_alias="totalTokens",
    )


class EmbeddingsResponse(AIModel):
    """Validated embeddings API response."""

    object: Literal["list"]
    data: list[EmbeddingItem]
    model: str
    usage: EmbeddingsUsage


class EmbedUsage(AIModel):
    """Simplified embedding usage returned by the SDK."""

    total_tokens: int = Field(alias="totalTokens")


class EmbedResult(AIModel):
    """Simplified embedding vectors and total token usage."""

    embeddings: list[list[float]]
    usage: EmbedUsage


class GenerateSpeechOptions(AIModel):
    text: str
    voice: str
    model: str | None = None
    speed: float | None = Field(default=None, ge=0.25, le=4.0)
    format: Literal["mp3", "wav", "opus"] | None = None


class GenerateImageOptions(AIModel):
    prompt: str
    model: str | None = None
    size: str | None = None
    quality: Literal["standard", "hd"] | None = None
    style: Literal["natural", "vivid"] | None = None
    n: int | None = Field(default=None, ge=1, le=10)


class GeneratedImage(AIModel):
    url: str | None = None
    b64_json: str | None = Field(default=None, alias="b64Json")


class GenerateImageResult(AIModel):
    images: list[GeneratedImage]


class GenerateVideoOptions(AIModel):
    prompt: str
    model: str | None = None
    duration: float | None = None
    resolution: str | None = None
    fps: float | None = None
    aspect_ratio: str | None = Field(default=None, alias="aspectRatio")


class GenerateVideoResult(AIModel):
    video_url: str = Field(alias="videoUrl")


class TranscriptionResult(AIModel):
    text: str


class TranscriptionOptions(AIModel):
    file: bytes
    filename: str = "audio"
    content_type: str = "application/octet-stream"
    model: str
    language: str | None = None
    prompt: str | None = None
    response_format: Literal["json", "text", "srt", "verbose_json", "vtt"] | None = (
        Field(default=None, alias="responseFormat")
    )
    temperature: float | None = None


class ModerationOptions(AIModel):
    input: str | list[str]
    model: str | None = None


class ModerationItem(AIModel):
    flagged: bool
    categories: dict[str, bool]
    category_scores: dict[str, float] = Field(alias="categoryScores")


class ModerationResult(AIModel):
    id: str
    model: str
    results: list[ModerationItem]


class RerankDocument(AIModel):
    content: str
    source_path: str | None = Field(default=None, alias="sourcePath")
    chunk_index: int | None = Field(default=None, alias="chunkIndex")
    metadata: dict[str, str] | None = None


class RerankOptions(AIModel):
    model: str
    query: str
    documents: list[str | RerankDocument]
    top_k: int | None = Field(default=None, alias="topK")
    criteria: str | None = None


class RerankResult(AIModel):
    scores: list[float]
    usage: JSONValue = None


class VariableDefinition(AIModel):
    type: Literal["string", "number", "boolean"]
    description: str | None = None
    default_value: str | float | bool | None = Field(default=None, alias="defaultValue")


class Prompt(AIModel):
    name: str
    template: str
    variables: dict[str, VariableDefinition]
    metadata: dict[str, JSONValue] | None = None
    version: str | None = None


class PromptChain(AIModel):
    prompts: list[Prompt]


ObjectT = TypeVar("ObjectT")


class GenerateObjectResult(AIModel, Generic[ObjectT]):
    object: ObjectT
    usage: TokenUsage


__all__ = [
    "ChatCompletionChoice",
    "ChatCompletionRequest",
    "ChatCompletionResponse",
    "ChatMessage",
    "EmbedResult",
    "EmbedUsage",
    "EmbeddingItem",
    "EmbeddingsRequest",
    "EmbeddingsResponse",
    "EmbeddingsUsage",
    "GenerateTextOptions",
    "GenerateTextResult",
    "StreamTextOptions",
    "TextStreamPart",
    "TextPart",
    "ToolCallPart",
    "FinishPart",
    "StreamErrorPart",
    "AbortPart",
    "DonePart",
    "GenerateImageOptions",
    "GenerateImageResult",
    "GeneratedImage",
    "GenerateObjectResult",
    "GenerateSpeechOptions",
    "GenerateVideoOptions",
    "GenerateVideoResult",
    "ModerationItem",
    "ModerationOptions",
    "ModerationResult",
    "Message",
    "Prompt",
    "PromptChain",
    "RerankDocument",
    "RerankOptions",
    "RerankResult",
    "TranscriptionResult",
    "TranscriptionOptions",
    "VariableDefinition",
    "TokenUsage",
    "ToolCall",
    "ToolDefinition",
    "ToolLoopStep",
    "ToolResult",
]

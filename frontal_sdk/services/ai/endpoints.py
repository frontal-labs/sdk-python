"""Generated endpoint catalog for the ai service."""

from frontal_sdk.utils.operation import Endpoint


class AiEndpoint(Endpoint):
    """Known ai API operations."""

    GET_HEALTH = ("GET", "/health")
    GET_INTERNAL_MODELS = ("GET", "/internal/models")
    GET_INTERNAL_MODELS_DEFAULTS = ("GET", "/internal/models/defaults")
    POST_AI_CHAT_COMPLETIONS = ("POST", "/ai/chat/completions")
    POST_INTERNAL_EMBEDDINGS = ("POST", "/internal/embeddings")
    POST_INTERNAL_PREDICTIONS = ("POST", "/internal/predictions")
    POST_INTERNAL_RERANK = ("POST", "/internal/rerank")
    POST_FORM_DATA_INTERNAL_PREDICTIONS = ("POSTFORMDATA", "/internal/predictions")
    POST_RAW_INTERNAL_PREDICTIONS = ("POSTRAW", "/internal/predictions")

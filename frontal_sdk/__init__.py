"""Python client library for the Frontal API."""

from frontal_sdk.client import Frontal
from frontal_sdk.core.config import ClientConfig
from frontal_sdk.core.errors import FrontalError
from frontal_sdk.models import (
    JSONObject,
    JSONPrimitive,
    JSONValue,
    MultipartPart,
    QueryParams,
    ServerEvent,
)

__version__ = "0.1.0"

__all__ = [
    "ClientConfig",
    "Frontal",
    "FrontalError",
    "MultipartPart",
    "JSONObject",
    "JSONPrimitive",
    "JSONValue",
    "QueryParams",
    "ServerEvent",
    "__version__",
]

"""Python client library for the Frontal API."""

from frontal_sdk.api_types import JSONObject, JSONPrimitive, JSONValue
from frontal_sdk.client import Frontal
from frontal_sdk.utils.config import ClientConfig
from frontal_sdk.utils.errors import FrontalError

__version__ = "0.1.0"

__all__ = [
    "ClientConfig",
    "Frontal",
    "FrontalError",
    "JSONObject",
    "JSONPrimitive",
    "JSONValue",
    "__version__",
]

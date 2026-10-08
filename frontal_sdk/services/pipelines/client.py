"""Typed endpoint client for the pipelines service."""

from frontal_sdk.services.base import BaseServiceClient
from frontal_sdk.services.pipelines.endpoints import PipelinesEndpoint


class PipelinesClient(BaseServiceClient[PipelinesEndpoint]):
    """Calls the catalogued pipelines operations."""

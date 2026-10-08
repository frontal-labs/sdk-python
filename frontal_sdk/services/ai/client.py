"""Typed endpoint client for the ai service."""

from frontal_sdk.services.ai.endpoints import AiEndpoint
from frontal_sdk.services.base import BaseServiceClient


class AiClient(BaseServiceClient[AiEndpoint]):
    """Calls the catalogued ai operations."""

"""Typed endpoint client for the agents service."""

from frontal_sdk.services.agents.endpoints import AgentsEndpoint
from frontal_sdk.services.base import BaseServiceClient


class AgentsClient(BaseServiceClient[AgentsEndpoint]):
    """Calls the catalogued agents operations."""

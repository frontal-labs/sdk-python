"""Typed endpoint client for the observability service."""

from frontal_sdk.services.base import BaseServiceClient
from frontal_sdk.services.observability.endpoints import ObservabilityEndpoint


class ObservabilityClient(BaseServiceClient[ObservabilityEndpoint]):
    """Calls the catalogued observability operations."""

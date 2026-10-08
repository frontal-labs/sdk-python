"""Typed endpoint client for the data service."""

from frontal_sdk.services.base import BaseServiceClient
from frontal_sdk.services.data.endpoints import DataEndpoint


class DataClient(BaseServiceClient[DataEndpoint]):
    """Calls the catalogued data operations."""

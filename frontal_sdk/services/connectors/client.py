"""Typed endpoint client for the connectors service."""

from frontal_sdk.services.base import BaseServiceClient
from frontal_sdk.services.connectors.endpoints import ConnectorsEndpoint


class ConnectorsClient(BaseServiceClient[ConnectorsEndpoint]):
    """Calls the catalogued connectors operations."""

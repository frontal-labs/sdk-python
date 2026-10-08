"""Typed endpoint client for the lineage service."""

from frontal_sdk.services.base import BaseServiceClient
from frontal_sdk.services.lineage.endpoints import LineageEndpoint


class LineageClient(BaseServiceClient[LineageEndpoint]):
    """Calls the catalogued lineage operations."""

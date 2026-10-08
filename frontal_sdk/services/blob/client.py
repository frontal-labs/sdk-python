"""Typed endpoint client for the blob service."""

from frontal_sdk.services.base import BaseServiceClient
from frontal_sdk.services.blob.endpoints import BlobEndpoint


class BlobClient(BaseServiceClient[BlobEndpoint]):
    """Calls the catalogued blob operations."""

"""Typed endpoint client for the sandbox service."""

from frontal_sdk.services.base import BaseServiceClient
from frontal_sdk.services.sandbox.endpoints import SandboxEndpoint


class SandboxClient(BaseServiceClient[SandboxEndpoint]):
    """Calls the catalogued sandbox operations."""

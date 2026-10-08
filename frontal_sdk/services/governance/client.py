"""Typed endpoint client for the governance service."""

from frontal_sdk.services.base import BaseServiceClient
from frontal_sdk.services.governance.endpoints import GovernanceEndpoint


class GovernanceClient(BaseServiceClient[GovernanceEndpoint]):
    """Calls the catalogued governance operations."""

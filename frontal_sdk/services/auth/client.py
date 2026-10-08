"""Typed endpoint client for the auth service."""

from frontal_sdk.services.auth.endpoints import AuthEndpoint
from frontal_sdk.services.base import BaseServiceClient


class AuthClient(BaseServiceClient[AuthEndpoint]):
    """Calls the catalogued auth operations."""

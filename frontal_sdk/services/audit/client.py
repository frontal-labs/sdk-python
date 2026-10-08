"""Typed endpoint client for the audit service."""

from frontal_sdk.services.audit.endpoints import AuditEndpoint
from frontal_sdk.services.base import BaseServiceClient


class AuditClient(BaseServiceClient[AuditEndpoint]):
    """Calls the catalogued audit operations."""

"""Typed endpoint client for the workflows service."""

from frontal_sdk.services.base import BaseServiceClient
from frontal_sdk.services.workflows.endpoints import WorkflowsEndpoint


class WorkflowsClient(BaseServiceClient[WorkflowsEndpoint]):
    """Calls the catalogued workflows operations."""

"""Typed endpoint client for the webhooks service."""

from frontal_sdk.services.base import BaseServiceClient
from frontal_sdk.services.webhooks.endpoints import WebhooksEndpoint


class WebhooksClient(BaseServiceClient[WebhooksEndpoint]):
    """Calls the catalogued webhooks operations."""

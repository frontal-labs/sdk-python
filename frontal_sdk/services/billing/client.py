"""Typed endpoint client for the billing service."""

from frontal_sdk.services.base import BaseServiceClient
from frontal_sdk.services.billing.endpoints import BillingEndpoint


class BillingClient(BaseServiceClient[BillingEndpoint]):
    """Calls the catalogued billing operations."""

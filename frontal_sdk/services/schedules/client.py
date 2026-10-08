"""Typed endpoint client for the schedules service."""

from frontal_sdk.services.base import BaseServiceClient
from frontal_sdk.services.schedules.endpoints import SchedulesEndpoint


class SchedulesClient(BaseServiceClient[SchedulesEndpoint]):
    """Calls the catalogued schedules operations."""

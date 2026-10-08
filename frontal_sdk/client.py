"""Unified Frontal API client."""

from __future__ import annotations

import os

from frontal_sdk.services.agents import AgentsClient
from frontal_sdk.services.ai import AiClient
from frontal_sdk.services.audit import AuditClient
from frontal_sdk.services.auth import AuthClient
from frontal_sdk.services.billing import BillingClient
from frontal_sdk.services.blob import BlobClient
from frontal_sdk.services.connectors import ConnectorsClient
from frontal_sdk.services.data import DataClient
from frontal_sdk.services.governance import GovernanceClient
from frontal_sdk.services.lineage import LineageClient
from frontal_sdk.services.observability import ObservabilityClient
from frontal_sdk.services.ontology import OntologyClient
from frontal_sdk.services.pipelines import PipelinesClient
from frontal_sdk.services.sandbox import SandboxClient
from frontal_sdk.services.schedules import SchedulesClient
from frontal_sdk.services.webhooks import WebhooksClient
from frontal_sdk.services.workflows import WorkflowsClient
from frontal_sdk.utils.config import ClientConfig
from frontal_sdk.utils.http import HttpClient


class Frontal:
    """Own one authenticated HTTP client and its service namespaces."""

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://api.frontal.dev/v1",
        timeout: float = 30.0,
        max_retries: int = 2,
        headers: dict[str, str] | None = None,
    ) -> None:
        config = ClientConfig(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            headers=headers or {},
        )
        self._http = HttpClient(config)
        self.agents = AgentsClient(self._http)
        self.ai = AiClient(self._http)
        self.audit = AuditClient(self._http)
        self.auth = AuthClient(self._http)
        self.billing = BillingClient(self._http)
        self.blob = BlobClient(self._http)
        self.connectors = ConnectorsClient(self._http)
        self.data = DataClient(self._http)
        self.governance = GovernanceClient(self._http)
        self.lineage = LineageClient(self._http)
        self.observability = ObservabilityClient(self._http)
        self.ontology = OntologyClient(self._http)
        self.pipelines = PipelinesClient(self._http)
        self.sandbox = SandboxClient(self._http)
        self.schedules = SchedulesClient(self._http)
        self.webhooks = WebhooksClient(self._http)
        self.workflows = WorkflowsClient(self._http)

    @classmethod
    def from_env(cls) -> Frontal:
        """Create a client from FRONTAL_API_KEY and optional FRONTAL_API_URL."""
        api_key = os.environ.get("FRONTAL_API_KEY")
        if not api_key:
            raise ValueError("FRONTAL_API_KEY is required")
        return cls(
            api_key,
            base_url=os.environ.get("FRONTAL_API_URL", "https://api.frontal.dev/v1"),
        )

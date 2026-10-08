"""Unified synchronous client for the Frontal API."""

from __future__ import annotations

import os
from collections.abc import Mapping

from frontal_sdk.core.config import ClientConfig
from frontal_sdk.core.http import HttpClient
from frontal_sdk.resources import (
    AI,
    Agents,
    Audit,
    Auth,
    Billing,
    Blob,
    Connectors,
    Data,
    Governance,
    Lineage,
    Observability,
    Ontology,
    Pipelines,
    Sandbox,
    Schedules,
    Webhooks,
    Workflows,
)


class Frontal:
    """Authenticated API client with typed resource namespaces.

    Args:
        api_key: Frontal API key.
        base_url: API base URL, including an optional version prefix.
        timeout: Per-request timeout in seconds.
        max_retries: Maximum retries for retryable GET responses.
        headers: Additional headers sent with every request.
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://api.frontal.dev/v1",
        timeout: float = 30.0,
        max_retries: int = 2,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        config = ClientConfig(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            headers=headers or {},
        )
        http = HttpClient(config)
        self.agents = Agents(http)
        self.ai = AI(http)
        self.audit = Audit(http)
        self.auth = Auth(http)
        self.billing = Billing(http)
        self.blob = Blob(http)
        self.connectors = Connectors(http)
        self.data = Data(http)
        self.governance = Governance(http)
        self.lineage = Lineage(http)
        self.observability = Observability(http)
        self.ontology = Ontology(http)
        self.pipelines = Pipelines(http)
        self.sandbox = Sandbox(http)
        self.schedules = Schedules(http)
        self.webhooks = Webhooks(http)
        self.workflows = Workflows(http)

    @classmethod
    def from_env(cls) -> Frontal:
        """Create a client from ``FRONTAL_API_KEY`` and optional ``FRONTAL_API_URL``."""
        api_key = os.environ.get("FRONTAL_API_KEY")
        if not api_key:
            raise ValueError("FRONTAL_API_KEY is required")
        return cls(
            api_key,
            base_url=os.environ.get("FRONTAL_API_URL", "https://api.frontal.dev/v1"),
        )

"""Typed endpoint client for the ontology service."""

from frontal_sdk.services.base import BaseServiceClient
from frontal_sdk.services.ontology.endpoints import OntologyEndpoint


class OntologyClient(BaseServiceClient[OntologyEndpoint]):
    """Calls the catalogued ontology operations."""

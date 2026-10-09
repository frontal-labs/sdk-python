"""Typed API resource for the ontology endpoints."""

from __future__ import annotations

from typing import Generic

from frontal_sdk.core.operation import Operation
from frontal_sdk.models import QueryParams
from frontal_sdk.models.requests import UNSET, RequestBodyInput
from frontal_sdk.resources._base import (
    APIResource,
    BytesResultT,
    JSONResultT,
    StreamResultT,
)


class Ontology(
    APIResource[JSONResultT, BytesResultT, StreamResultT],
    Generic[JSONResultT, BytesResultT, StreamResultT],
):
    """Methods for the ontology API endpoints."""

    def delete_object_type(
        self, object_type_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /ontology/objects/object-types/{param}."""
        return self._request(
            Operation("DELETE", "/ontology/objects/object-types/{param}"),
            path_params=(object_type_id,),
            query=query,
        )

    def delete_object(
        self, object_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /ontology/objects/objects/{param}."""
        return self._request(
            Operation("DELETE", "/ontology/objects/objects/{param}"),
            path_params=(object_id,),
            query=query,
        )

    def delete_reasoning_rule(
        self, rule_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /ontology/reasoning/rules/{param}."""
        return self._request(
            Operation("DELETE", "/ontology/reasoning/rules/{param}"),
            path_params=(rule_id,),
            query=query,
        )

    def delete_relationship_type(
        self, relationship_type_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /ontology/relationships/relationship-types/{param}."""
        return self._request(
            Operation("DELETE", "/ontology/relationships/relationship-types/{param}"),
            path_params=(relationship_type_id,),
            query=query,
        )

    def delete_relationship(
        self, relationship_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /ontology/relationships/relationships/{param}."""
        return self._request(
            Operation("DELETE", "/ontology/relationships/relationships/{param}"),
            path_params=(relationship_id,),
            query=query,
        )

    def delete_rollout(
        self, rollout_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /ontology/rollouts/rollouts/{param}."""
        return self._request(
            Operation("DELETE", "/ontology/rollouts/rollouts/{param}"),
            path_params=(rollout_id,),
            query=query,
        )

    def delete_rollup(
        self, rollup_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /ontology/rollups/rollups/{param}."""
        return self._request(
            Operation("DELETE", "/ontology/rollups/rollups/{param}"),
            path_params=(rollup_id,),
            query=query,
        )

    def delete_schema(
        self, schema_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /ontology/schemas/schemas/{param}."""
        return self._request(
            Operation("DELETE", "/ontology/schemas/schemas/{param}"),
            path_params=(schema_id,),
            query=query,
        )

    def delete_validation_rule(
        self, rule_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /ontology/validation/rules/{param}."""
        return self._request(
            Operation("DELETE", "/ontology/validation/rules/{param}"),
            path_params=(rule_id,),
            query=query,
        )

    def delete_version(
        self, version_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /ontology/versions/versions/{param}."""
        return self._request(
            Operation("DELETE", "/ontology/versions/versions/{param}"),
            path_params=(version_id,),
            query=query,
        )

    def list_events(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /ontology/events/events."""
        return self._request(
            Operation("GET", "/ontology/events/events"),
            path_params=(),
            query=query,
        )

    def get_event(
        self, event_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /ontology/events/events/{param}."""
        return self._request(
            Operation("GET", "/ontology/events/events/{param}"),
            path_params=(event_id,),
            query=query,
        )

    def get_consumer(
        self, consumer: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /ontology/events/events/checkpoints/{param}."""
        return self._request(
            Operation("GET", "/ontology/events/events/checkpoints/{param}"),
            path_params=(consumer,),
            query=query,
        )

    def list_object_types(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /ontology/objects/object-types."""
        return self._request(
            Operation("GET", "/ontology/objects/object-types"),
            path_params=(),
            query=query,
        )

    def get_object_type(
        self, object_type_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /ontology/objects/object-types/{param}."""
        return self._request(
            Operation("GET", "/ontology/objects/object-types/{param}"),
            path_params=(object_type_id,),
            query=query,
        )

    def list_objects(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /ontology/objects/objects."""
        return self._request(
            Operation("GET", "/ontology/objects/objects"),
            path_params=(),
            query=query,
        )

    def get_object(
        self, object_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /ontology/objects/objects/{param}."""
        return self._request(
            Operation("GET", "/ontology/objects/objects/{param}"),
            path_params=(object_id,),
            query=query,
        )

    def list_reasoning_rules(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /ontology/reasoning/rules."""
        return self._request(
            Operation("GET", "/ontology/reasoning/rules"),
            path_params=(),
            query=query,
        )

    def list_relationship_types(
        self, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /ontology/relationships/relationship-types."""
        return self._request(
            Operation("GET", "/ontology/relationships/relationship-types"),
            path_params=(),
            query=query,
        )

    def list_relationships(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /ontology/relationships/relationships."""
        return self._request(
            Operation("GET", "/ontology/relationships/relationships"),
            path_params=(),
            query=query,
        )

    def get_relationship(
        self, relationship_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /ontology/relationships/relationships/{param}."""
        return self._request(
            Operation("GET", "/ontology/relationships/relationships/{param}"),
            path_params=(relationship_id,),
            query=query,
        )

    def list_rollouts(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /ontology/rollouts/rollouts."""
        return self._request(
            Operation("GET", "/ontology/rollouts/rollouts"),
            path_params=(),
            query=query,
        )

    def get_rollout(
        self, rollout_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /ontology/rollouts/rollouts/{param}."""
        return self._request(
            Operation("GET", "/ontology/rollouts/rollouts/{param}"),
            path_params=(rollout_id,),
            query=query,
        )

    def list_rollout_status(
        self, rollout_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /ontology/rollouts/rollouts/{param}/status."""
        return self._request(
            Operation("GET", "/ontology/rollouts/rollouts/{param}/status"),
            path_params=(rollout_id,),
            query=query,
        )

    def get_execution(
        self, execution_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /ontology/rollups/rollup-results/{param}."""
        return self._request(
            Operation("GET", "/ontology/rollups/rollup-results/{param}"),
            path_params=(execution_id,),
            query=query,
        )

    def list_rollups(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /ontology/rollups/rollups."""
        return self._request(
            Operation("GET", "/ontology/rollups/rollups"),
            path_params=(),
            query=query,
        )

    def get_rollup(
        self, rollup_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /ontology/rollups/rollups/{param}."""
        return self._request(
            Operation("GET", "/ontology/rollups/rollups/{param}"),
            path_params=(rollup_id,),
            query=query,
        )

    def get_rollup_result(
        self, rollup_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /ontology/rollups/rollups/{param}/result."""
        return self._request(
            Operation("GET", "/ontology/rollups/rollups/{param}/result"),
            path_params=(rollup_id,),
            query=query,
        )

    def list_schemas(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /ontology/schemas/schemas."""
        return self._request(
            Operation("GET", "/ontology/schemas/schemas"),
            path_params=(),
            query=query,
        )

    def get_schema(
        self, schema_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /ontology/schemas/schemas/{param}."""
        return self._request(
            Operation("GET", "/ontology/schemas/schemas/{param}"),
            path_params=(schema_id,),
            query=query,
        )

    def list_validation_rules(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /ontology/validation/rules."""
        return self._request(
            Operation("GET", "/ontology/validation/rules"),
            path_params=(),
            query=query,
        )

    def get_rule(
        self, rule_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /ontology/validation/rules/{param}."""
        return self._request(
            Operation("GET", "/ontology/validation/rules/{param}"),
            path_params=(rule_id,),
            query=query,
        )

    def list_release_bundles(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /ontology/versions/release-bundles."""
        return self._request(
            Operation("GET", "/ontology/versions/release-bundles"),
            path_params=(),
            query=query,
        )

    def get_bundle(
        self, bundle_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /ontology/versions/release-bundles/{param}."""
        return self._request(
            Operation("GET", "/ontology/versions/release-bundles/{param}"),
            path_params=(bundle_id,),
            query=query,
        )

    def get_version(
        self, version_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /ontology/versions/versions/{param}."""
        return self._request(
            Operation("GET", "/ontology/versions/versions/{param}"),
            path_params=(version_id,),
            query=query,
        )

    def create_compare_version(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/engine/ontologies/compare-versions."""
        return self._request(
            Operation("POST", "/ontology/engine/ontologies/compare-versions"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_ontology_engine_ontologies_export(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/engine/ontologies/export."""
        return self._request(
            Operation("POST", "/ontology/engine/ontologies/export"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_ontology_engine_ontologies_export_shacl(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/engine/ontologies/export-shacl."""
        return self._request(
            Operation("POST", "/ontology/engine/ontologies/export-shacl"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_ontology_engine_ontologies_generate(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/engine/ontologies/generate."""
        return self._request(
            Operation("POST", "/ontology/engine/ontologies/generate"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_infer_class(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/engine/ontologies/infer-classes."""
        return self._request(
            Operation("POST", "/ontology/engine/ontologies/infer-classes"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_infer_property(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/engine/ontologies/infer-properties."""
        return self._request(
            Operation("POST", "/ontology/engine/ontologies/infer-properties"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_ontology_engine_ontologies_validate(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/engine/ontologies/validate."""
        return self._request(
            Operation("POST", "/ontology/engine/ontologies/validate"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_event(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/events/events."""
        return self._request(
            Operation("POST", "/ontology/events/events"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_checkpoint(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/events/events/checkpoints."""
        return self._request(
            Operation("POST", "/ontology/events/events/checkpoints"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_ontology_events_events_leases_acknowledge(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/events/events/leases/acknowledge."""
        return self._request(
            Operation("POST", "/ontology/events/events/leases/acknowledge"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_ontology_events_events_leases_acquire(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/events/events/leases/acquire."""
        return self._request(
            Operation("POST", "/ontology/events/events/leases/acquire"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_ontology_extract_extract_analyze(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/extract/extract/analyze."""
        return self._request(
            Operation("POST", "/ontology/extract/extract/analyze"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_ontology_extract_extract_architecture(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/extract/extract/architecture."""
        return self._request(
            Operation("POST", "/ontology/extract/extract/architecture"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_coreference(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/extract/extract/coreferences."""
        return self._request(
            Operation("POST", "/ontology/extract/extract/coreferences"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_entity(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/extract/extract/entities."""
        return self._request(
            Operation("POST", "/ontology/extract/extract/entities"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_extract_event(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/extract/extract/events."""
        return self._request(
            Operation("POST", "/ontology/extract/extract/events"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_relation(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/extract/extract/relations."""
        return self._request(
            Operation("POST", "/ontology/extract/extract/relations"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_triplet(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/extract/extract/triplets."""
        return self._request(
            Operation("POST", "/ontology/extract/extract/triplets"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_ontology_reasoning_explain(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/reasoning/explain."""
        return self._request(
            Operation("POST", "/ontology/reasoning/explain"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_fact(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/reasoning/facts."""
        return self._request(
            Operation("POST", "/ontology/reasoning/facts"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_ontology_reasoning_facts_load_graph(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/reasoning/facts/load-graph."""
        return self._request(
            Operation("POST", "/ontology/reasoning/facts/load-graph"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_ontology_reasoning_reason_backward(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/reasoning/reason/backward."""
        return self._request(
            Operation("POST", "/ontology/reasoning/reason/backward"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_ontology_reasoning_reason_forward(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/reasoning/reason/forward."""
        return self._request(
            Operation("POST", "/ontology/reasoning/reason/forward"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_reasoning_rule(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/reasoning/rules."""
        return self._request(
            Operation("POST", "/ontology/reasoning/rules"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_rollout(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/rollouts/rollouts."""
        return self._request(
            Operation("POST", "/ontology/rollouts/rollouts"),
            path_params=(),
            query=query,
            body=body,
        )

    def pause_rollout(
        self,
        rollout_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /ontology/rollouts/rollouts/{param}/pause."""
        return self._request(
            Operation("POST", "/ontology/rollouts/rollouts/{param}/pause"),
            path_params=(rollout_id,),
            query=query,
            body=body,
        )

    def resume_rollout(
        self,
        rollout_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /ontology/rollouts/rollouts/{param}/resume."""
        return self._request(
            Operation("POST", "/ontology/rollouts/rollouts/{param}/resume"),
            path_params=(rollout_id,),
            query=query,
            body=body,
        )

    def rollback_rollout(
        self,
        rollout_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /ontology/rollouts/rollouts/{param}/rollback."""
        return self._request(
            Operation("POST", "/ontology/rollouts/rollouts/{param}/rollback"),
            path_params=(rollout_id,),
            query=query,
            body=body,
        )

    def start_rollout(
        self,
        rollout_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /ontology/rollouts/rollouts/{param}/start."""
        return self._request(
            Operation("POST", "/ontology/rollouts/rollouts/{param}/start"),
            path_params=(rollout_id,),
            query=query,
            body=body,
        )

    def create_rollup(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/rollups/rollups."""
        return self._request(
            Operation("POST", "/ontology/rollups/rollups"),
            path_params=(),
            query=query,
            body=body,
        )

    def execute_rollup(
        self,
        rollup_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /ontology/rollups/rollups/{param}/execute."""
        return self._request(
            Operation("POST", "/ontology/rollups/rollups/{param}/execute"),
            path_params=(rollup_id,),
            query=query,
            body=body,
        )

    def preview_rollup(
        self,
        rollup_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /ontology/rollups/rollups/{param}/preview."""
        return self._request(
            Operation("POST", "/ontology/rollups/rollups/{param}/preview"),
            path_params=(rollup_id,),
            query=query,
            body=body,
        )

    def create_schema(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/schemas/schemas."""
        return self._request(
            Operation("POST", "/ontology/schemas/schemas"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_ontology_schemas_schemas_validate(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/schemas/schemas/validate."""
        return self._request(
            Operation("POST", "/ontology/schemas/schemas/validate"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_transformation(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/transformations/transformations."""
        return self._request(
            Operation("POST", "/ontology/transformations/transformations"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_ontology_validation_payloads_validate(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/validation/payloads/validate."""
        return self._request(
            Operation("POST", "/ontology/validation/payloads/validate"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_validation_rule(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/validation/rules."""
        return self._request(
            Operation("POST", "/ontology/validation/rules"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_ontology_versions_audit_verify(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/versions/audit/verify."""
        return self._request(
            Operation("POST", "/ontology/versions/audit/verify"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_release_bundle(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/versions/release-bundles."""
        return self._request(
            Operation("POST", "/ontology/versions/release-bundles"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_version(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/versions/versions."""
        return self._request(
            Operation("POST", "/ontology/versions/versions"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_ontology_versions_versions_compare(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /ontology/versions/versions/compare."""
        return self._request(
            Operation("POST", "/ontology/versions/versions/compare"),
            path_params=(),
            query=query,
            body=body,
        )

    def update_object_type(
        self,
        object_type_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call PUT /ontology/objects/object-types/{param}."""
        return self._request(
            Operation("PUT", "/ontology/objects/object-types/{param}"),
            path_params=(object_type_id,),
            query=query,
            body=body,
        )

    def update_object(
        self,
        object_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call PUT /ontology/objects/objects/{param}."""
        return self._request(
            Operation("PUT", "/ontology/objects/objects/{param}"),
            path_params=(object_id,),
            query=query,
            body=body,
        )

    def update_rule(
        self,
        rule_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call PUT /ontology/reasoning/rules/{param}."""
        return self._request(
            Operation("PUT", "/ontology/reasoning/rules/{param}"),
            path_params=(rule_id,),
            query=query,
            body=body,
        )

    def update_relationship(
        self,
        relationship_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call PUT /ontology/relationships/relationships/{param}."""
        return self._request(
            Operation("PUT", "/ontology/relationships/relationships/{param}"),
            path_params=(relationship_id,),
            query=query,
            body=body,
        )

    def update_rollout(
        self,
        rollout_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call PUT /ontology/rollouts/rollouts/{param}."""
        return self._request(
            Operation("PUT", "/ontology/rollouts/rollouts/{param}"),
            path_params=(rollout_id,),
            query=query,
            body=body,
        )

    def update_rollup(
        self,
        rollup_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call PUT /ontology/rollups/rollups/{param}."""
        return self._request(
            Operation("PUT", "/ontology/rollups/rollups/{param}"),
            path_params=(rollup_id,),
            query=query,
            body=body,
        )

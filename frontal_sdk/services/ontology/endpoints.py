"""Generated endpoint catalog for the ontology service."""

from frontal_sdk.utils.operation import Endpoint


class OntologyEndpoint(Endpoint):
    """Known ontology API operations."""

    DELETE_ONTOLOGY_OBJECTS_OBJECT_TYPES_PARAM_1 = (
        "DELETE",
        "/ontology/objects/object-types/{param}",
    )
    DELETE_ONTOLOGY_OBJECTS_OBJECTS_PARAM_1 = (
        "DELETE",
        "/ontology/objects/objects/{param}",
    )
    DELETE_ONTOLOGY_REASONING_RULES_PARAM_1 = (
        "DELETE",
        "/ontology/reasoning/rules/{param}",
    )
    DELETE_ONTOLOGY_RELATIONSHIPS_RELATIONSHIP_TYPES_PARAM_1 = (
        "DELETE",
        "/ontology/relationships/relationship-types/{param}",
    )
    DELETE_ONTOLOGY_RELATIONSHIPS_RELATIONSHIPS_PARAM_1 = (
        "DELETE",
        "/ontology/relationships/relationships/{param}",
    )
    DELETE_ONTOLOGY_ROLLOUTS_ROLLOUTS_PARAM_1 = (
        "DELETE",
        "/ontology/rollouts/rollouts/{param}",
    )
    DELETE_ONTOLOGY_ROLLUPS_ROLLUPS_PARAM_1 = (
        "DELETE",
        "/ontology/rollups/rollups/{param}",
    )
    DELETE_ONTOLOGY_SCHEMAS_SCHEMAS_PARAM_1 = (
        "DELETE",
        "/ontology/schemas/schemas/{param}",
    )
    DELETE_ONTOLOGY_VALIDATION_RULES_PARAM_1 = (
        "DELETE",
        "/ontology/validation/rules/{param}",
    )
    DELETE_ONTOLOGY_VERSIONS_VERSIONS_PARAM_1 = (
        "DELETE",
        "/ontology/versions/versions/{param}",
    )
    GET_ONTOLOGY_EVENTS_EVENTS = ("GET", "/ontology/events/events")
    GET_ONTOLOGY_EVENTS_EVENTS_PARAM_1 = ("GET", "/ontology/events/events/{param}")
    GET_ONTOLOGY_EVENTS_EVENTS_CHECKPOINTS_PARAM_1 = (
        "GET",
        "/ontology/events/events/checkpoints/{param}",
    )
    GET_ONTOLOGY_OBJECTS_OBJECT_TYPES = ("GET", "/ontology/objects/object-types")
    GET_ONTOLOGY_OBJECTS_OBJECT_TYPES_PARAM_1 = (
        "GET",
        "/ontology/objects/object-types/{param}",
    )
    GET_ONTOLOGY_OBJECTS_OBJECTS = ("GET", "/ontology/objects/objects")
    GET_ONTOLOGY_OBJECTS_OBJECTS_PARAM_1 = ("GET", "/ontology/objects/objects/{param}")
    GET_ONTOLOGY_REASONING_RULES = ("GET", "/ontology/reasoning/rules")
    GET_ONTOLOGY_RELATIONSHIPS_RELATIONSHIP_TYPES = (
        "GET",
        "/ontology/relationships/relationship-types",
    )
    GET_ONTOLOGY_RELATIONSHIPS_RELATIONSHIPS = (
        "GET",
        "/ontology/relationships/relationships",
    )
    GET_ONTOLOGY_RELATIONSHIPS_RELATIONSHIPS_PARAM_1 = (
        "GET",
        "/ontology/relationships/relationships/{param}",
    )
    GET_ONTOLOGY_ROLLOUTS_ROLLOUTS = ("GET", "/ontology/rollouts/rollouts")
    GET_ONTOLOGY_ROLLOUTS_ROLLOUTS_PARAM_1 = (
        "GET",
        "/ontology/rollouts/rollouts/{param}",
    )
    GET_ONTOLOGY_ROLLOUTS_ROLLOUTS_PARAM_1_STATUS = (
        "GET",
        "/ontology/rollouts/rollouts/{param}/status",
    )
    GET_ONTOLOGY_ROLLUPS_ROLLUP_RESULTS_PARAM_1 = (
        "GET",
        "/ontology/rollups/rollup-results/{param}",
    )
    GET_ONTOLOGY_ROLLUPS_ROLLUPS = ("GET", "/ontology/rollups/rollups")
    GET_ONTOLOGY_ROLLUPS_ROLLUPS_PARAM_1 = ("GET", "/ontology/rollups/rollups/{param}")
    GET_ONTOLOGY_ROLLUPS_ROLLUPS_PARAM_1_RESULT = (
        "GET",
        "/ontology/rollups/rollups/{param}/result",
    )
    GET_ONTOLOGY_SCHEMAS_SCHEMAS = ("GET", "/ontology/schemas/schemas")
    GET_ONTOLOGY_SCHEMAS_SCHEMAS_PARAM_1 = ("GET", "/ontology/schemas/schemas/{param}")
    GET_ONTOLOGY_VALIDATION_RULES = ("GET", "/ontology/validation/rules")
    GET_ONTOLOGY_VALIDATION_RULES_PARAM_1 = (
        "GET",
        "/ontology/validation/rules/{param}",
    )
    GET_ONTOLOGY_VERSIONS_RELEASE_BUNDLES = (
        "GET",
        "/ontology/versions/release-bundles",
    )
    GET_ONTOLOGY_VERSIONS_RELEASE_BUNDLES_PARAM_1 = (
        "GET",
        "/ontology/versions/release-bundles/{param}",
    )
    GET_ONTOLOGY_VERSIONS_VERSIONS_PARAM_1 = (
        "GET",
        "/ontology/versions/versions/{param}",
    )
    POST_ONTOLOGY_ENGINE_ONTOLOGIES_COMPARE_VERSIONS = (
        "POST",
        "/ontology/engine/ontologies/compare-versions",
    )
    POST_ONTOLOGY_ENGINE_ONTOLOGIES_EXPORT = (
        "POST",
        "/ontology/engine/ontologies/export",
    )
    POST_ONTOLOGY_ENGINE_ONTOLOGIES_EXPORT_SHACL = (
        "POST",
        "/ontology/engine/ontologies/export-shacl",
    )
    POST_ONTOLOGY_ENGINE_ONTOLOGIES_GENERATE = (
        "POST",
        "/ontology/engine/ontologies/generate",
    )
    POST_ONTOLOGY_ENGINE_ONTOLOGIES_INFER_CLASSES = (
        "POST",
        "/ontology/engine/ontologies/infer-classes",
    )
    POST_ONTOLOGY_ENGINE_ONTOLOGIES_INFER_PROPERTIES = (
        "POST",
        "/ontology/engine/ontologies/infer-properties",
    )
    POST_ONTOLOGY_ENGINE_ONTOLOGIES_VALIDATE = (
        "POST",
        "/ontology/engine/ontologies/validate",
    )
    POST_ONTOLOGY_EVENTS_EVENTS = ("POST", "/ontology/events/events")
    POST_ONTOLOGY_EVENTS_EVENTS_CHECKPOINTS = (
        "POST",
        "/ontology/events/events/checkpoints",
    )
    POST_ONTOLOGY_EVENTS_EVENTS_LEASES_ACKNOWLEDGE = (
        "POST",
        "/ontology/events/events/leases/acknowledge",
    )
    POST_ONTOLOGY_EVENTS_EVENTS_LEASES_ACQUIRE = (
        "POST",
        "/ontology/events/events/leases/acquire",
    )
    POST_ONTOLOGY_EXTRACT_EXTRACT_ANALYZE = (
        "POST",
        "/ontology/extract/extract/analyze",
    )
    POST_ONTOLOGY_EXTRACT_EXTRACT_ARCHITECTURE = (
        "POST",
        "/ontology/extract/extract/architecture",
    )
    POST_ONTOLOGY_EXTRACT_EXTRACT_COREFERENCES = (
        "POST",
        "/ontology/extract/extract/coreferences",
    )
    POST_ONTOLOGY_EXTRACT_EXTRACT_ENTITIES = (
        "POST",
        "/ontology/extract/extract/entities",
    )
    POST_ONTOLOGY_EXTRACT_EXTRACT_EVENTS = ("POST", "/ontology/extract/extract/events")
    POST_ONTOLOGY_EXTRACT_EXTRACT_RELATIONS = (
        "POST",
        "/ontology/extract/extract/relations",
    )
    POST_ONTOLOGY_EXTRACT_EXTRACT_TRIPLETS = (
        "POST",
        "/ontology/extract/extract/triplets",
    )
    POST_ONTOLOGY_REASONING_EXPLAIN = ("POST", "/ontology/reasoning/explain")
    POST_ONTOLOGY_REASONING_FACTS = ("POST", "/ontology/reasoning/facts")
    POST_ONTOLOGY_REASONING_FACTS_LOAD_GRAPH = (
        "POST",
        "/ontology/reasoning/facts/load-graph",
    )
    POST_ONTOLOGY_REASONING_REASON_BACKWARD = (
        "POST",
        "/ontology/reasoning/reason/backward",
    )
    POST_ONTOLOGY_REASONING_REASON_FORWARD = (
        "POST",
        "/ontology/reasoning/reason/forward",
    )
    POST_ONTOLOGY_REASONING_RULES = ("POST", "/ontology/reasoning/rules")
    POST_ONTOLOGY_ROLLOUTS_ROLLOUTS = ("POST", "/ontology/rollouts/rollouts")
    POST_ONTOLOGY_ROLLOUTS_ROLLOUTS_PARAM_1_PAUSE = (
        "POST",
        "/ontology/rollouts/rollouts/{param}/pause",
    )
    POST_ONTOLOGY_ROLLOUTS_ROLLOUTS_PARAM_1_RESUME = (
        "POST",
        "/ontology/rollouts/rollouts/{param}/resume",
    )
    POST_ONTOLOGY_ROLLOUTS_ROLLOUTS_PARAM_1_ROLLBACK = (
        "POST",
        "/ontology/rollouts/rollouts/{param}/rollback",
    )
    POST_ONTOLOGY_ROLLOUTS_ROLLOUTS_PARAM_1_START = (
        "POST",
        "/ontology/rollouts/rollouts/{param}/start",
    )
    POST_ONTOLOGY_ROLLUPS_ROLLUPS = ("POST", "/ontology/rollups/rollups")
    POST_ONTOLOGY_ROLLUPS_ROLLUPS_PARAM_1_EXECUTE = (
        "POST",
        "/ontology/rollups/rollups/{param}/execute",
    )
    POST_ONTOLOGY_ROLLUPS_ROLLUPS_PARAM_1_PREVIEW = (
        "POST",
        "/ontology/rollups/rollups/{param}/preview",
    )
    POST_ONTOLOGY_SCHEMAS_SCHEMAS = ("POST", "/ontology/schemas/schemas")
    POST_ONTOLOGY_SCHEMAS_SCHEMAS_VALIDATE = (
        "POST",
        "/ontology/schemas/schemas/validate",
    )
    POST_ONTOLOGY_TRANSFORMATIONS_TRANSFORMATIONS = (
        "POST",
        "/ontology/transformations/transformations",
    )
    POST_ONTOLOGY_VALIDATION_PAYLOADS_VALIDATE = (
        "POST",
        "/ontology/validation/payloads/validate",
    )
    POST_ONTOLOGY_VALIDATION_RULES = ("POST", "/ontology/validation/rules")
    POST_ONTOLOGY_VERSIONS_AUDIT_VERIFY = ("POST", "/ontology/versions/audit/verify")
    POST_ONTOLOGY_VERSIONS_RELEASE_BUNDLES = (
        "POST",
        "/ontology/versions/release-bundles",
    )
    POST_ONTOLOGY_VERSIONS_VERSIONS = ("POST", "/ontology/versions/versions")
    POST_ONTOLOGY_VERSIONS_VERSIONS_COMPARE = (
        "POST",
        "/ontology/versions/versions/compare",
    )
    PUT_ONTOLOGY_OBJECTS_OBJECT_TYPES_PARAM_1 = (
        "PUT",
        "/ontology/objects/object-types/{param}",
    )
    PUT_ONTOLOGY_OBJECTS_OBJECTS_PARAM_1 = ("PUT", "/ontology/objects/objects/{param}")
    PUT_ONTOLOGY_REASONING_RULES_PARAM_1 = ("PUT", "/ontology/reasoning/rules/{param}")
    PUT_ONTOLOGY_RELATIONSHIPS_RELATIONSHIPS_PARAM_1 = (
        "PUT",
        "/ontology/relationships/relationships/{param}",
    )
    PUT_ONTOLOGY_ROLLOUTS_ROLLOUTS_PARAM_1 = (
        "PUT",
        "/ontology/rollouts/rollouts/{param}",
    )
    PUT_ONTOLOGY_ROLLUPS_ROLLUPS_PARAM_1 = ("PUT", "/ontology/rollups/rollups/{param}")

"""Generated endpoint catalog for the data service."""

from frontal_sdk.utils.operation import Endpoint


class DataEndpoint(Endpoint):
    """Known data API operations."""

    GET_DATA_AGGREGATIONS_AGGREGATIONS = ("GET", "/data/aggregations/aggregations")
    GET_DATA_AGGREGATIONS_AGGREGATIONS_PARAM_1 = (
        "GET",
        "/data/aggregations/aggregations/{param}",
    )
    GET_DATA_ARCHIVAL_ARCHIVAL_POLICIES = ("GET", "/data/archival/archival/policies")
    GET_DATA_ARCHIVAL_ARCHIVAL_POLICIES_PARAM_1 = (
        "GET",
        "/data/archival/archival/policies/{param}",
    )
    GET_DATA_ENRICHMENT_ENRICHMENT_PROFILES = (
        "GET",
        "/data/enrichment/enrichment/profiles",
    )
    GET_DATA_ENRICHMENT_ENRICHMENT_PROFILES_PARAM_1 = (
        "GET",
        "/data/enrichment/enrichment/profiles/{param}",
    )
    GET_DATA_EXPORTS_EXPORTS = ("GET", "/data/exports/exports")
    GET_DATA_EXPORTS_EXPORTS_PARAM_1 = ("GET", "/data/exports/exports/{param}")
    GET_DATA_NORMALIZATION_NORMALIZATION_PROFILES = (
        "GET",
        "/data/normalization/normalization/profiles",
    )
    GET_DATA_NORMALIZATION_NORMALIZATION_PROFILES_PARAM_1 = (
        "GET",
        "/data/normalization/normalization/profiles/{param}",
    )
    GET_DATA_QUALITY_QUALITY_RULESETS = ("GET", "/data/quality/quality/rulesets")
    GET_DATA_QUALITY_QUALITY_RULESETS_PARAM_1 = (
        "GET",
        "/data/quality/quality/rulesets/{param}",
    )
    GET_DATA_SCHEMAS_SCHEMAS = ("GET", "/data/schemas/schemas")
    GET_DATA_SCHEMAS_SCHEMAS_PARAM_1 = ("GET", "/data/schemas/schemas/{param}")
    GET_DATA_SERVING_SERVING_PRODUCTS = ("GET", "/data/serving/serving/products")
    GET_DATA_SERVING_SERVING_PRODUCTS_PARAM_1 = (
        "GET",
        "/data/serving/serving/products/{param}",
    )
    GET_DATA_STREAMS_STREAMS = ("GET", "/data/streams/streams")
    GET_DATA_STREAMS_STREAMS_PARAM_1 = ("GET", "/data/streams/streams/{param}")
    GET_DATA_SYNC_SYNC_JOBS = ("GET", "/data/sync/sync/jobs")
    GET_DATA_SYNC_SYNC_JOBS_PARAM_1 = ("GET", "/data/sync/sync/jobs/{param}")
    GET_DATA_TRANSFORMATIONS_TRANSFORMATIONS = (
        "GET",
        "/data/transformations/transformations",
    )
    GET_DATA_TRANSFORMATIONS_TRANSFORMATIONS_PARAM_1 = (
        "GET",
        "/data/transformations/transformations/{param}",
    )
    POST_DATA_AGGREGATIONS_AGGREGATIONS = ("POST", "/data/aggregations/aggregations")
    POST_DATA_AGGREGATIONS_AGGREGATIONS_PARAM_1_EXECUTIONS = (
        "POST",
        "/data/aggregations/aggregations/{param}/executions",
    )
    POST_DATA_ARCHIVAL_ARCHIVAL_POLICIES = ("POST", "/data/archival/archival/policies")
    POST_DATA_ARCHIVAL_ARCHIVAL_POLICIES_PARAM_1_EXECUTIONS = (
        "POST",
        "/data/archival/archival/policies/{param}/executions",
    )
    POST_DATA_ENRICHMENT_ENRICHMENT_PROFILES = (
        "POST",
        "/data/enrichment/enrichment/profiles",
    )
    POST_DATA_ENRICHMENT_ENRICHMENT_PROFILES_PARAM_1_EXECUTIONS = (
        "POST",
        "/data/enrichment/enrichment/profiles/{param}/executions",
    )
    POST_DATA_EXPORTS_EXPORTS = ("POST", "/data/exports/exports")
    POST_DATA_EXPORTS_EXPORTS_PARAM_1_EXECUTIONS = (
        "POST",
        "/data/exports/exports/{param}/executions",
    )
    POST_DATA_NORMALIZATION_NORMALIZATION_PROFILES = (
        "POST",
        "/data/normalization/normalization/profiles",
    )
    POST_DATA_NORMALIZATION_NORMALIZATION_PROFILES_PARAM_1_EXECUTIONS = (
        "POST",
        "/data/normalization/normalization/profiles/{param}/executions",
    )
    POST_DATA_QUALITY_QUALITY_RULESETS = ("POST", "/data/quality/quality/rulesets")
    POST_DATA_QUALITY_QUALITY_RULESETS_PARAM_1_EVALUATIONS = (
        "POST",
        "/data/quality/quality/rulesets/{param}/evaluations",
    )
    POST_DATA_QUERY_QUERY_FEDERATED = ("POST", "/data/query/query/federated")
    POST_DATA_SCHEMAS_SCHEMAS = ("POST", "/data/schemas/schemas")
    POST_DATA_SCHEMAS_SCHEMAS_RESOLVE = ("POST", "/data/schemas/schemas/resolve")
    POST_DATA_SERVING_SERVING_PRODUCTS = ("POST", "/data/serving/serving/products")
    POST_DATA_SERVING_SERVING_PRODUCTS_PARAM_1_REFRESHES = (
        "POST",
        "/data/serving/serving/products/{param}/refreshes",
    )
    POST_DATA_STREAMS_STREAMS = ("POST", "/data/streams/streams")
    POST_DATA_STREAMS_STREAMS_PARAM_1_DELIVERIES = (
        "POST",
        "/data/streams/streams/{param}/deliveries",
    )
    POST_DATA_SYNC_SYNC_JOBS = ("POST", "/data/sync/sync/jobs")
    POST_DATA_SYNC_SYNC_JOBS_PARAM_1_EXECUTIONS = (
        "POST",
        "/data/sync/sync/jobs/{param}/executions",
    )
    POST_DATA_TRANSFORMATIONS_TRANSFORMATIONS = (
        "POST",
        "/data/transformations/transformations",
    )
    POST_DATA_TRANSFORMATIONS_TRANSFORMATIONS_PARAM_1_EXECUTIONS = (
        "POST",
        "/data/transformations/transformations/{param}/executions",
    )

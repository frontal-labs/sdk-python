"""Typed API resource for the data endpoints."""

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


class Data(
    APIResource[JSONResultT, BytesResultT, StreamResultT],
    Generic[JSONResultT, BytesResultT, StreamResultT],
):
    """Methods for the data API endpoints."""

    def list_aggregations(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /data/aggregations/aggregations."""
        return self._request(
            Operation("GET", "/data/aggregations/aggregations"),
            path_params=(),
            query=query,
        )

    def get_aggregation(
        self, aggregation_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /data/aggregations/aggregations/{param}."""
        return self._request(
            Operation("GET", "/data/aggregations/aggregations/{param}"),
            path_params=(aggregation_id,),
            query=query,
        )

    def list_policies(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /data/archival/archival/policies."""
        return self._request(
            Operation("GET", "/data/archival/archival/policies"),
            path_params=(),
            query=query,
        )

    def get_policy(
        self, policy_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /data/archival/archival/policies/{param}."""
        return self._request(
            Operation("GET", "/data/archival/archival/policies/{param}"),
            path_params=(policy_id,),
            query=query,
        )

    def list_enrichment_profiles(
        self, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /data/enrichment/enrichment/profiles."""
        return self._request(
            Operation("GET", "/data/enrichment/enrichment/profiles"),
            path_params=(),
            query=query,
        )

    def get_enrichment_profile(
        self, profile_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /data/enrichment/enrichment/profiles/{param}."""
        return self._request(
            Operation("GET", "/data/enrichment/enrichment/profiles/{param}"),
            path_params=(profile_id,),
            query=query,
        )

    def list_exports(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /data/exports/exports."""
        return self._request(
            Operation("GET", "/data/exports/exports"),
            path_params=(),
            query=query,
        )

    def get_export(
        self, export_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /data/exports/exports/{param}."""
        return self._request(
            Operation("GET", "/data/exports/exports/{param}"),
            path_params=(export_id,),
            query=query,
        )

    def list_normalization_profiles(
        self, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /data/normalization/normalization/profiles."""
        return self._request(
            Operation("GET", "/data/normalization/normalization/profiles"),
            path_params=(),
            query=query,
        )

    def get_normalization_profile(
        self, profile_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /data/normalization/normalization/profiles/{param}."""
        return self._request(
            Operation("GET", "/data/normalization/normalization/profiles/{param}"),
            path_params=(profile_id,),
            query=query,
        )

    def list_rulesets(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /data/quality/quality/rulesets."""
        return self._request(
            Operation("GET", "/data/quality/quality/rulesets"),
            path_params=(),
            query=query,
        )

    def get_ruleset(
        self, ruleset_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /data/quality/quality/rulesets/{param}."""
        return self._request(
            Operation("GET", "/data/quality/quality/rulesets/{param}"),
            path_params=(ruleset_id,),
            query=query,
        )

    def list_schemas(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /data/schemas/schemas."""
        return self._request(
            Operation("GET", "/data/schemas/schemas"),
            path_params=(),
            query=query,
        )

    def get_schema_ref(
        self, schema_ref: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /data/schemas/schemas/{param}."""
        return self._request(
            Operation("GET", "/data/schemas/schemas/{param}"),
            path_params=(schema_ref,),
            query=query,
        )

    def list_products(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /data/serving/serving/products."""
        return self._request(
            Operation("GET", "/data/serving/serving/products"),
            path_params=(),
            query=query,
        )

    def get_product(
        self, product_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /data/serving/serving/products/{param}."""
        return self._request(
            Operation("GET", "/data/serving/serving/products/{param}"),
            path_params=(product_id,),
            query=query,
        )

    def list_streams(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /data/streams/streams."""
        return self._request(
            Operation("GET", "/data/streams/streams"),
            path_params=(),
            query=query,
        )

    def get_stream(
        self, stream_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /data/streams/streams/{param}."""
        return self._request(
            Operation("GET", "/data/streams/streams/{param}"),
            path_params=(stream_id,),
            query=query,
        )

    def list_jobs(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /data/sync/sync/jobs."""
        return self._request(
            Operation("GET", "/data/sync/sync/jobs"),
            path_params=(),
            query=query,
        )

    def get_job(self, job_id: str, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /data/sync/sync/jobs/{param}."""
        return self._request(
            Operation("GET", "/data/sync/sync/jobs/{param}"),
            path_params=(job_id,),
            query=query,
        )

    def list_transformations(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /data/transformations/transformations."""
        return self._request(
            Operation("GET", "/data/transformations/transformations"),
            path_params=(),
            query=query,
        )

    def get_transformation(
        self, transformation_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /data/transformations/transformations/{param}."""
        return self._request(
            Operation("GET", "/data/transformations/transformations/{param}"),
            path_params=(transformation_id,),
            query=query,
        )

    def create_aggregation(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /data/aggregations/aggregations."""
        return self._request(
            Operation("POST", "/data/aggregations/aggregations"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_execution_for_aggregation(
        self,
        aggregation_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /data/aggregations/aggregations/{param}/executions."""
        return self._request(
            Operation("POST", "/data/aggregations/aggregations/{param}/executions"),
            path_params=(aggregation_id,),
            query=query,
            body=body,
        )

    def create_policy(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /data/archival/archival/policies."""
        return self._request(
            Operation("POST", "/data/archival/archival/policies"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_execution_for_policy(
        self,
        policy_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /data/archival/archival/policies/{param}/executions."""
        return self._request(
            Operation("POST", "/data/archival/archival/policies/{param}/executions"),
            path_params=(policy_id,),
            query=query,
            body=body,
        )

    def create_enrichment_profile(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /data/enrichment/enrichment/profiles."""
        return self._request(
            Operation("POST", "/data/enrichment/enrichment/profiles"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_execution_for_enrichment_profile(
        self,
        profile_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /data/enrichment/enrichment/profiles/{param}/executions."""
        return self._request(
            Operation(
                "POST", "/data/enrichment/enrichment/profiles/{param}/executions"
            ),
            path_params=(profile_id,),
            query=query,
            body=body,
        )

    def create_export(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /data/exports/exports."""
        return self._request(
            Operation("POST", "/data/exports/exports"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_execution_for_export(
        self,
        export_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /data/exports/exports/{param}/executions."""
        return self._request(
            Operation("POST", "/data/exports/exports/{param}/executions"),
            path_params=(export_id,),
            query=query,
            body=body,
        )

    def create_normalization_profile(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /data/normalization/normalization/profiles."""
        return self._request(
            Operation("POST", "/data/normalization/normalization/profiles"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_execution_for_normalization_profile(
        self,
        profile_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /data/normalization/normalization/profiles/{param}/executions."""
        return self._request(
            Operation(
                "POST", "/data/normalization/normalization/profiles/{param}/executions"
            ),
            path_params=(profile_id,),
            query=query,
            body=body,
        )

    def create_ruleset(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /data/quality/quality/rulesets."""
        return self._request(
            Operation("POST", "/data/quality/quality/rulesets"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_evaluation_for_ruleset(
        self,
        ruleset_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /data/quality/quality/rulesets/{param}/evaluations."""
        return self._request(
            Operation("POST", "/data/quality/quality/rulesets/{param}/evaluations"),
            path_params=(ruleset_id,),
            query=query,
            body=body,
        )

    def post_data_query_query_federated(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /data/query/query/federated."""
        return self._request(
            Operation("POST", "/data/query/query/federated"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_schema(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /data/schemas/schemas."""
        return self._request(
            Operation("POST", "/data/schemas/schemas"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_data_schemas_schemas_resolve(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /data/schemas/schemas/resolve."""
        return self._request(
            Operation("POST", "/data/schemas/schemas/resolve"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_product(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /data/serving/serving/products."""
        return self._request(
            Operation("POST", "/data/serving/serving/products"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_refresh_for_product(
        self,
        product_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /data/serving/serving/products/{param}/refreshes."""
        return self._request(
            Operation("POST", "/data/serving/serving/products/{param}/refreshes"),
            path_params=(product_id,),
            query=query,
            body=body,
        )

    def create_stream(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /data/streams/streams."""
        return self._request(
            Operation("POST", "/data/streams/streams"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_delivery_for_stream(
        self,
        stream_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /data/streams/streams/{param}/deliveries."""
        return self._request(
            Operation("POST", "/data/streams/streams/{param}/deliveries"),
            path_params=(stream_id,),
            query=query,
            body=body,
        )

    def create_job(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /data/sync/sync/jobs."""
        return self._request(
            Operation("POST", "/data/sync/sync/jobs"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_execution_for_job(
        self,
        job_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /data/sync/sync/jobs/{param}/executions."""
        return self._request(
            Operation("POST", "/data/sync/sync/jobs/{param}/executions"),
            path_params=(job_id,),
            query=query,
            body=body,
        )

    def create_transformation(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /data/transformations/transformations."""
        return self._request(
            Operation("POST", "/data/transformations/transformations"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_execution_for_transformation(
        self,
        transformation_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /data/transformations/transformations/{param}/executions."""
        return self._request(
            Operation(
                "POST", "/data/transformations/transformations/{param}/executions"
            ),
            path_params=(transformation_id,),
            query=query,
            body=body,
        )

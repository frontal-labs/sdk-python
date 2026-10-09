"""Typed API resource for the governance endpoints."""

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


class Governance(
    APIResource[JSONResultT, BytesResultT, StreamResultT],
    Generic[JSONResultT, BytesResultT, StreamResultT],
):
    """Methods for the governance API endpoints."""

    def delete_policy(
        self, policy_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /policies/{param}."""
        return self._request(
            Operation("DELETE", "/policies/{param}"),
            path_params=(policy_id,),
            query=query,
        )

    def delete_role(
        self, role_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /roles/{param}."""
        return self._request(
            Operation("DELETE", "/roles/{param}"),
            path_params=(role_id,),
            query=query,
        )

    def list_assessments(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /compliance/assessments."""
        return self._request(
            Operation("GET", "/compliance/assessments"),
            path_params=(),
            query=query,
        )

    def get_assessment(
        self, assessment_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /compliance/assessments/{param}."""
        return self._request(
            Operation("GET", "/compliance/assessments/{param}"),
            path_params=(assessment_id,),
            query=query,
        )

    def list_frameworks(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /compliance/frameworks."""
        return self._request(
            Operation("GET", "/compliance/frameworks"),
            path_params=(),
            query=query,
        )

    def get_compliance_score(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /compliance/score."""
        return self._request(
            Operation("GET", "/compliance/score"),
            path_params=(),
            query=query,
        )

    def list_violations(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /compliance/violations."""
        return self._request(
            Operation("GET", "/compliance/violations"),
            path_params=(),
            query=query,
        )

    def list_permissions(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /permissions."""
        return self._request(
            Operation("GET", "/permissions"),
            path_params=(),
            query=query,
        )

    def get_permission(
        self, permission_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /permissions/{param}."""
        return self._request(
            Operation("GET", "/permissions/{param}"),
            path_params=(permission_id,),
            query=query,
        )

    def list_policies(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /policies."""
        return self._request(
            Operation("GET", "/policies"),
            path_params=(),
            query=query,
        )

    def get_policy(
        self, policy_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /policies/{param}."""
        return self._request(
            Operation("GET", "/policies/{param}"),
            path_params=(policy_id,),
            query=query,
        )

    def list_policy_versions(
        self, policy_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /policies/{param}/versions."""
        return self._request(
            Operation("GET", "/policies/{param}/versions"),
            path_params=(policy_id,),
            query=query,
        )

    def list_templates(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /policies/templates."""
        return self._request(
            Operation("GET", "/policies/templates"),
            path_params=(),
            query=query,
        )

    def list_roles(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /roles."""
        return self._request(
            Operation("GET", "/roles"),
            path_params=(),
            query=query,
        )

    def get_role(
        self, role_id: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /roles/{param}."""
        return self._request(
            Operation("GET", "/roles/{param}"),
            path_params=(role_id,),
            query=query,
        )

    def post_access_check(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /access/check."""
        return self._request(
            Operation("POST", "/access/check"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_assessment(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /compliance/assessments."""
        return self._request(
            Operation("POST", "/compliance/assessments"),
            path_params=(),
            query=query,
            body=body,
        )

    def resolve_violation(
        self,
        violation_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call POST /compliance/violations/{param}/resolve."""
        return self._request(
            Operation("POST", "/compliance/violations/{param}/resolve"),
            path_params=(violation_id,),
            query=query,
            body=body,
        )

    def create_permission(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /permissions."""
        return self._request(
            Operation("POST", "/permissions"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_policy(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /policies."""
        return self._request(
            Operation("POST", "/policies"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_policies_from_template(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /policies/from-template."""
        return self._request(
            Operation("POST", "/policies/from-template"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_policies_validate(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /policies/validate."""
        return self._request(
            Operation("POST", "/policies/validate"),
            path_params=(),
            query=query,
            body=body,
        )

    def create_role(
        self, *, query: QueryParams | None = None, body: RequestBodyInput = UNSET
    ) -> JSONResultT:
        """Call POST /roles."""
        return self._request(
            Operation("POST", "/roles"),
            path_params=(),
            query=query,
            body=body,
        )

    def update_policy(
        self,
        policy_id: str,
        *,
        query: QueryParams | None = None,
        body: RequestBodyInput = UNSET,
    ) -> JSONResultT:
        """Call PUT /policies/{param}."""
        return self._request(
            Operation("PUT", "/policies/{param}"),
            path_params=(policy_id,),
            query=query,
            body=body,
        )

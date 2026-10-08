"""Typed API resource for the governance endpoints."""

from __future__ import annotations

from typing import Generic

from frontal_sdk.core.operation import Operation
from frontal_sdk.models import QueryParams, RequestBody
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

    def delete_policies_by_param_1(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /policies/{param}."""
        return self._request(
            Operation("DELETE", "/policies/{param}"),
            path_params=(param_1,),
            query=query,
        )

    def delete_roles_by_param_1(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call DELETE /roles/{param}."""
        return self._request(
            Operation("DELETE", "/roles/{param}"),
            path_params=(param_1,),
            query=query,
        )

    def get_compliance_assessments(
        self, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /compliance/assessments."""
        return self._request(
            Operation("GET", "/compliance/assessments"),
            path_params=(),
            query=query,
        )

    def get_compliance_assessments_by_param_1(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /compliance/assessments/{param}."""
        return self._request(
            Operation("GET", "/compliance/assessments/{param}"),
            path_params=(param_1,),
            query=query,
        )

    def get_compliance_frameworks(
        self, *, query: QueryParams | None = None
    ) -> JSONResultT:
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

    def get_compliance_violations(
        self, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /compliance/violations."""
        return self._request(
            Operation("GET", "/compliance/violations"),
            path_params=(),
            query=query,
        )

    def get_permissions(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /permissions."""
        return self._request(
            Operation("GET", "/permissions"),
            path_params=(),
            query=query,
        )

    def get_permissions_by_param_1(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /permissions/{param}."""
        return self._request(
            Operation("GET", "/permissions/{param}"),
            path_params=(param_1,),
            query=query,
        )

    def get_policies(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /policies."""
        return self._request(
            Operation("GET", "/policies"),
            path_params=(),
            query=query,
        )

    def get_policies_by_param_1(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /policies/{param}."""
        return self._request(
            Operation("GET", "/policies/{param}"),
            path_params=(param_1,),
            query=query,
        )

    def get_policies_by_param_1_versions(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /policies/{param}/versions."""
        return self._request(
            Operation("GET", "/policies/{param}/versions"),
            path_params=(param_1,),
            query=query,
        )

    def get_policies_templates(
        self, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /policies/templates."""
        return self._request(
            Operation("GET", "/policies/templates"),
            path_params=(),
            query=query,
        )

    def get_roles(self, *, query: QueryParams | None = None) -> JSONResultT:
        """Call GET /roles."""
        return self._request(
            Operation("GET", "/roles"),
            path_params=(),
            query=query,
        )

    def get_roles_by_param_1(
        self, param_1: str, *, query: QueryParams | None = None
    ) -> JSONResultT:
        """Call GET /roles/{param}."""
        return self._request(
            Operation("GET", "/roles/{param}"),
            path_params=(param_1,),
            query=query,
        )

    def post_access_check(
        self, *, query: QueryParams | None = None, body: RequestBody = None
    ) -> JSONResultT:
        """Call POST /access/check."""
        return self._request(
            Operation("POST", "/access/check"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_compliance_assessments(
        self, *, query: QueryParams | None = None, body: RequestBody = None
    ) -> JSONResultT:
        """Call POST /compliance/assessments."""
        return self._request(
            Operation("POST", "/compliance/assessments"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_compliance_violations_by_param_1_resolve(
        self,
        param_1: str,
        *,
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONResultT:
        """Call POST /compliance/violations/{param}/resolve."""
        return self._request(
            Operation("POST", "/compliance/violations/{param}/resolve"),
            path_params=(param_1,),
            query=query,
            body=body,
        )

    def post_permissions(
        self, *, query: QueryParams | None = None, body: RequestBody = None
    ) -> JSONResultT:
        """Call POST /permissions."""
        return self._request(
            Operation("POST", "/permissions"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_policies(
        self, *, query: QueryParams | None = None, body: RequestBody = None
    ) -> JSONResultT:
        """Call POST /policies."""
        return self._request(
            Operation("POST", "/policies"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_policies_from_template(
        self, *, query: QueryParams | None = None, body: RequestBody = None
    ) -> JSONResultT:
        """Call POST /policies/from-template."""
        return self._request(
            Operation("POST", "/policies/from-template"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_policies_validate(
        self, *, query: QueryParams | None = None, body: RequestBody = None
    ) -> JSONResultT:
        """Call POST /policies/validate."""
        return self._request(
            Operation("POST", "/policies/validate"),
            path_params=(),
            query=query,
            body=body,
        )

    def post_roles(
        self, *, query: QueryParams | None = None, body: RequestBody = None
    ) -> JSONResultT:
        """Call POST /roles."""
        return self._request(
            Operation("POST", "/roles"),
            path_params=(),
            query=query,
            body=body,
        )

    def put_policies_by_param_1(
        self,
        param_1: str,
        *,
        query: QueryParams | None = None,
        body: RequestBody = None,
    ) -> JSONResultT:
        """Call PUT /policies/{param}."""
        return self._request(
            Operation("PUT", "/policies/{param}"),
            path_params=(param_1,),
            query=query,
            body=body,
        )

"""Generated endpoint catalog for the governance service."""

from frontal_sdk.utils.operation import Endpoint


class GovernanceEndpoint(Endpoint):
    """Known governance API operations."""

    DELETE_POLICIES_PARAM_1 = ("DELETE", "/policies/{param}")
    DELETE_ROLES_PARAM_1 = ("DELETE", "/roles/{param}")
    GET_COMPLIANCE_ASSESSMENTS = ("GET", "/compliance/assessments")
    GET_COMPLIANCE_ASSESSMENTS_PARAM_1 = ("GET", "/compliance/assessments/{param}")
    GET_COMPLIANCE_FRAMEWORKS = ("GET", "/compliance/frameworks")
    GET_COMPLIANCE_SCORE = ("GET", "/compliance/score")
    GET_COMPLIANCE_VIOLATIONS = ("GET", "/compliance/violations")
    GET_PERMISSIONS = ("GET", "/permissions")
    GET_PERMISSIONS_PARAM_1 = ("GET", "/permissions/{param}")
    GET_POLICIES = ("GET", "/policies")
    GET_POLICIES_PARAM_1 = ("GET", "/policies/{param}")
    GET_POLICIES_PARAM_1_VERSIONS = ("GET", "/policies/{param}/versions")
    GET_POLICIES_TEMPLATES = ("GET", "/policies/templates")
    GET_ROLES = ("GET", "/roles")
    GET_ROLES_PARAM_1 = ("GET", "/roles/{param}")
    POST_ACCESS_CHECK = ("POST", "/access/check")
    POST_COMPLIANCE_ASSESSMENTS = ("POST", "/compliance/assessments")
    POST_COMPLIANCE_VIOLATIONS_PARAM_1_RESOLVE = (
        "POST",
        "/compliance/violations/{param}/resolve",
    )
    POST_PERMISSIONS = ("POST", "/permissions")
    POST_POLICIES = ("POST", "/policies")
    POST_POLICIES_FROM_TEMPLATE = ("POST", "/policies/from-template")
    POST_POLICIES_VALIDATE = ("POST", "/policies/validate")
    POST_ROLES = ("POST", "/roles")
    PUT_POLICIES_PARAM_1 = ("PUT", "/policies/{param}")

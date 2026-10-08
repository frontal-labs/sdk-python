"""Generated endpoint catalog for the audit service."""

from frontal_sdk.utils.operation import Endpoint


class AuditEndpoint(Endpoint):
    """Known audit API operations."""

    GET_AUDIT_EVENTS = ("GET", "/audit/events")
    GET_AUDIT_EVENTS_PARAM_1 = ("GET", "/audit/events/{param}")
    POST_AUDIT_EVENTS = ("POST", "/audit/events")
    POST_AUDIT_EVENTS_BATCH = ("POST", "/audit/events/batch")

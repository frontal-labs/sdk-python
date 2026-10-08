"""Generated endpoint catalog for the webhooks service."""

from frontal_sdk.utils.operation import Endpoint


class WebhooksEndpoint(Endpoint):
    """Known webhooks API operations."""

    DELETE_WEBHOOKS_PARAM_1 = ("DELETE", "/webhooks/{param}")
    GET_WEBHOOKS = ("GET", "/webhooks")
    GET_WEBHOOKS_PARAM_1 = ("GET", "/webhooks/{param}")
    GET_WEBHOOKS_DELIVERIES = ("GET", "/webhooks/deliveries")
    GET_WEBHOOKS_DELIVERIES_PARAM_1 = ("GET", "/webhooks/deliveries/{param}")
    GET_WEBHOOKS_STATS = ("GET", "/webhooks/stats")
    POST_WEBHOOKS = ("POST", "/webhooks")
    POST_WEBHOOKS_PARAM_1_ROTATE_SECRET = ("POST", "/webhooks/{param}/rotate-secret")
    POST_WEBHOOKS_DELIVERIES_PARAM_1_RETRY = (
        "POST",
        "/webhooks/deliveries/{param}/retry",
    )
    PUT_WEBHOOKS_PARAM_1 = ("PUT", "/webhooks/{param}")

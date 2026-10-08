"""Generated endpoint catalog for the sandbox service."""

from frontal_sdk.utils.operation import Endpoint


class SandboxEndpoint(Endpoint):
    """Known sandbox API operations."""

    GET_SANDBOX_LANGUAGES = ("GET", "/sandbox/languages")
    POST_SANDBOX_SELF_TEST = ("POST", "/sandbox/self-test")
    POST_SANDBOX_SUBMIT = ("POST", "/sandbox/submit")

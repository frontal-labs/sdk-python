"""Generated endpoint catalog for the blob service."""

from frontal_sdk.utils.operation import Endpoint


class BlobEndpoint(Endpoint):
    """Known blob API operations."""

    DELETE_BLOB_OBJECT_PARAM_1_PARAM_2 = ("DELETE", "/blob/object/{param}/{param}")
    GET_BLOB_OBJECT_INFO_PARAM_1_PARAM_2 = ("GET", "/blob/object/info/{param}/{param}")
    GET_BLOB_OBJECT_PARAM_1_PARAM_2 = ("GET", "/blob/object/{param}/{param}")
    POST_BLOB_OBJECT_COPY = ("POST", "/blob/object/copy")
    POST_BLOB_OBJECT_LIST_PARAM_1 = ("POST", "/blob/object/list/{param}")
    POST_BLOB_OBJECT_MOVE = ("POST", "/blob/object/move")
    POST_BLOB_OBJECT_SIGN_PARAM_1_PARAM_2 = (
        "POST",
        "/blob/object/sign/{param}/{param}",
    )
    POST_FORM_DATA_BLOB_OBJECT_PARAM_1_PARAM_2 = (
        "POSTFORMDATA",
        "/blob/object/{param}/{param}",
    )

"""Generated endpoint catalog for the lineage service."""

from frontal_sdk.utils.operation import Endpoint


class LineageEndpoint(Endpoint):
    """Known lineage API operations."""

    GET_LINEAGE_EDGES = ("GET", "/lineage/edges")
    GET_LINEAGE_EDGES_PARAM_1 = ("GET", "/lineage/edges/{param}")
    GET_LINEAGE_GRAPH = ("GET", "/lineage/graph")
    GET_LINEAGE_NODES = ("GET", "/lineage/nodes")
    GET_LINEAGE_NODES_PARAM_1 = ("GET", "/lineage/nodes/{param}")
    GET_LINEAGE_NODES_PARAM_1_TRACE = ("GET", "/lineage/nodes/{param}/trace")
    POST_LINEAGE_IMPACT = ("POST", "/lineage/impact")

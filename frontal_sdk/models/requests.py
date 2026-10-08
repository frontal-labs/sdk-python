"""Shared request boundary types for resource methods."""

from collections.abc import Mapping
from typing import Union

from pydantic import BaseModel

from frontal_sdk.models.types import JSONValue

QueryValue = Union[str, int, float, bool]
QueryParams = Mapping[str, QueryValue]
RequestBody = Union[JSONValue, BaseModel]

__all__ = ["QueryParams", "QueryValue", "RequestBody"]

"""Shared request boundary types for resource methods."""

from collections.abc import Mapping
from typing import TypeAlias

QueryValue: TypeAlias = str | int | float | bool
QueryParams: TypeAlias = Mapping[str, QueryValue]

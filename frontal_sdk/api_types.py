"""Public JSON value types used at the Frontal API boundary."""

from typing import TypeAlias

JSONPrimitive: TypeAlias = str | int | float | bool | None
JSONValue: TypeAlias = JSONPrimitive | list["JSONValue"] | dict[str, "JSONValue"]
JSONObject: TypeAlias = dict[str, JSONValue]

__all__ = ["JSONObject", "JSONPrimitive", "JSONValue"]

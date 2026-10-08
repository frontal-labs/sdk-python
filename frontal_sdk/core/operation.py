"""Immutable operation descriptors used by generated resource methods."""

from __future__ import annotations

from dataclasses import dataclass
from re import findall, sub
from urllib.parse import quote


@dataclass(frozen=True, slots=True)
class Operation:
    method: str
    path: str

    def __post_init__(self) -> None:
        if self.method not in {
            "GET",
            "GETRAW",
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
            "STREAM",
            "POSTFORMDATA",
            "POSTRAW",
        }:
            raise ValueError(f"unsupported HTTP method: {self.method}")
        if not self.path.startswith("/"):
            raise ValueError("operation paths must start with '/'")

    def render_path(self, parameters: tuple[str, ...]) -> str:
        placeholders = findall(r"\{[^{}]+\}", self.path.split("?", 1)[0])
        if len(parameters) != len(placeholders):
            raise ValueError(
                f"{self.method} {self.path} requires {len(placeholders)} path "
                f"parameters, received {len(parameters)}"
            )
        path = self.path
        for value in parameters:
            path = sub(r"\{[^{}]+\}", quote(value, safe=""), path, count=1)
        return path

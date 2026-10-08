"""Client configuration with validation at construction time."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from math import isfinite
from types import MappingProxyType
from urllib.parse import urlsplit


@dataclass(frozen=True, slots=True)
class ClientConfig:
    api_key: str
    base_url: str = "https://api.frontal.dev/v1"
    timeout: float = 30.0
    max_retries: int = 2
    headers: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        parsed = urlsplit(self.base_url)
        if not self.api_key.strip():
            raise ValueError("api_key must not be empty")
        if (
            parsed.scheme not in {"http", "https"}
            or not parsed.netloc
            or parsed.username is not None
            or parsed.password is not None
            or parsed.query
            or parsed.fragment
        ):
            raise ValueError(
                "base_url must be an absolute HTTP(S) URL without credentials, "
                "query, or fragment"
            )
        if not isfinite(self.timeout) or self.timeout <= 0:
            raise ValueError("timeout must be a finite positive number")
        if isinstance(self.max_retries, bool) or not isinstance(self.max_retries, int):
            raise TypeError("max_retries must be an integer")
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        for name, value in self.headers.items():
            if not name or any(char in name for char in "\r\n:"):
                raise ValueError(
                    "header names must be non-empty and contain no colon or newline"
                )
            if "\r" in value or "\n" in value:
                raise ValueError("header values must not contain newlines")
        object.__setattr__(self, "base_url", self.base_url.rstrip("/"))
        object.__setattr__(self, "headers", MappingProxyType(dict(self.headers)))

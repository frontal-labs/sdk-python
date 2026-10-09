"""Client configuration with validation at construction time."""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from math import isfinite
from types import MappingProxyType
from urllib.parse import urlsplit

_API_KEY_PATTERN = re.compile(r"frt_[A-Za-z0-9_-]+")


def _validate_api_key(api_key: str) -> None:
    if len(api_key) < 9 or _API_KEY_PATTERN.fullmatch(api_key) is None:
        raise ValueError(
            "api_key must start with 'frt_' and contain base64url characters"
        )


def _validate_base_url(base_url: str) -> None:
    parsed = urlsplit(base_url)
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


def _validate_retries(max_retries: int) -> None:
    if isinstance(max_retries, bool) or not isinstance(max_retries, int):
        raise TypeError("max_retries must be an integer")
    if not 0 <= max_retries <= 10:
        raise ValueError("max_retries must be between 0 and 10")


def _validate_headers(headers: Mapping[str, str]) -> None:
    reserved_headers = {
        "authorization",
        "x-request-id",
        "x-frontal-environment",
    }
    for name, value in headers.items():
        if not isinstance(name, str) or not isinstance(value, str):
            raise TypeError("header names and values must be strings")
        if not name or any(char in name for char in "\r\n:"):
            raise ValueError(
                "header names must be non-empty and contain no colon or newline"
            )
        if "\r" in value or "\n" in value:
            raise ValueError("header values must not contain newlines")
        if name.lower() in reserved_headers:
            raise ValueError(f"{name} is managed by the SDK and cannot be overridden")


@dataclass(frozen=True)
class ClientConfig:
    api_key: str
    base_url: str = "https://api.frontal.dev/v1"
    timeout: float = 30.0
    max_retries: int = 3
    headers: Mapping[str, str] = field(default_factory=dict)
    environment: str = "production"
    debug: bool = False

    def __post_init__(self) -> None:
        _validate_api_key(self.api_key)
        _validate_base_url(self.base_url)
        if not isfinite(self.timeout) or self.timeout <= 0:
            raise ValueError("timeout must be a finite positive number")
        _validate_retries(self.max_retries)
        if not self.environment.strip():
            raise ValueError("environment must not be empty")
        _validate_headers(self.headers)
        object.__setattr__(self, "base_url", self.base_url.rstrip("/"))
        object.__setattr__(self, "headers", MappingProxyType(dict(self.headers)))

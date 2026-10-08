"""Client configuration with validation at construction time."""

from __future__ import annotations

from dataclasses import dataclass, field
from urllib.parse import urlsplit


@dataclass(frozen=True, slots=True)
class ClientConfig:
    api_key: str
    base_url: str = "https://api.frontal.dev/v1"
    timeout: float = 30.0
    max_retries: int = 2
    headers: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        parsed = urlsplit(self.base_url)
        if not self.api_key.strip():
            raise ValueError("api_key must not be empty")
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("base_url must be an absolute HTTP(S) URL")
        if self.timeout <= 0:
            raise ValueError("timeout must be positive")
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        object.__setattr__(self, "base_url", self.base_url.rstrip("/"))
        object.__setattr__(self, "headers", dict(self.headers))

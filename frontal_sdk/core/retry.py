"""Retry backoff strategies shared by the transports."""

from __future__ import annotations

import random
from math import isfinite
from typing import Literal

from frontal_sdk.core.constants import EXPONENTIAL_BASE, JITTER_MAX

BackoffStrategy = Literal["exponential", "linear", "constant"]


def calculate_delay(
    attempt: int,
    *,
    strategy: BackoffStrategy = "exponential",
    base_delay: float = 1.0,
    jitter: bool = True,
) -> float:
    """Return the delay in seconds before retrying ``attempt``.

    ``exponential`` grows by ``base_delay * 2**attempt``, ``linear`` by
    ``base_delay * (attempt + 1)``, and ``constant`` stays at
    ``base_delay``. Jitter adds up to ``JITTER_MAX`` seconds to spread
    concurrent retries.
    """
    if isinstance(attempt, bool) or not isinstance(attempt, int):
        raise TypeError("attempt must be an integer")
    if attempt < 0:
        raise ValueError("attempt must be non-negative")
    if strategy not in {"exponential", "linear", "constant"}:
        raise ValueError("unsupported backoff strategy")
    if not isfinite(base_delay) or base_delay < 0:
        raise ValueError("base_delay must be a finite non-negative number")
    if strategy == "linear":
        delay = base_delay * (attempt + 1)
    elif strategy == "constant":
        delay = base_delay
    else:
        delay = base_delay * float(EXPONENTIAL_BASE**attempt)
    if not jitter:
        return delay
    return delay + random.uniform(0.0, JITTER_MAX)


__all__ = ["BackoffStrategy", "calculate_delay"]

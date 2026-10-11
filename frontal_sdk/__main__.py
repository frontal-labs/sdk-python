"""Allow running the Frontal Python SDK as a module: ``python -m frontal_sdk``.

This is useful for quick diagnostics, testing, and documentation purposes.
"""
from __future__ import annotations

import sys
from frontal_sdk import __version__, Frontal

DEFAULT_API_KEY_ENV = "FRONTAL_API_KEY"


def _check_api_key() -> bool:
    """Check if a Frontal API key is available in the environment."""
    import os
    return bool(
        os.environ.get("FRONTAL_API_KEY")
        or os.environ.get("FRONTAL_API_KEY_OLD")
    )


def main() -> None:
    """Entry point for ``python -m frontal_sdk``."""
    print(f"Frontal Python SDK v{__version__}")
    print("=" * 40)

    has_key = _check_api_key()
    if has_key:
        print("✓ Frontal API key detected in environment variables")
    else:
        print("⚠ No Frontal API key found (set FRONTAL_API_KEY)")
        print("  Set FRONTAL_API_KEY to a key starting with 'frt_'")
        print("  to make live API calls.")

    print()
    print("Available services:")
    services = [
        "agents",
        "ai",
        "workflows",
        "functions",
        "audit",
        "auth",
        "billing",
        "blob",
        "connectors",
        "data",
        "governance",
        "lineage",
        "observability",
        "ontology",
        "pipelines",
        "schedules",
        "webhooks",
    ]
    for svc in services:
        print(f"  - {svc}")

    print()
    print("Use ``from frontal_sdk import Frontal`` to start coding.")
    print("See ``https://frontal.dev/docs/python`` for the full documentation.")


if __name__ == "__main__":  # pragma: no cover
    main()
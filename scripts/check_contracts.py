#!/usr/bin/env python3
"""Validate that committed OpenAPI and endpoint contract snapshots are readable."""

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ROOT / "contracts/sdk-endpoints.json",
    ROOT / "contracts/coverage-floor.json",
    ROOT / "contracts/openapi/api.openapi.json",
    ROOT / "contracts/openapi/ai.openapi.generated.json",
    ROOT / "contracts/openapi/manifest.json",
]
for path in FILES:
    if not path.is_file():
        raise SystemExit(f"missing contract file: {path.relative_to(ROOT)}")
    with path.open(encoding="utf-8") as stream:
        json.load(stream)

inventory = json.loads(
    (ROOT / "contracts/sdk-endpoints.json").read_text(encoding="utf-8")
)
expected_count = 0
for domain, operations in inventory.items():
    resource_path = ROOT / "frontal_sdk/resources" / f"{domain}.py"
    if not operations:
        if resource_path.exists():
            raise SystemExit(f"unexpected resource module for empty domain: {domain}")
        continue
    if not resource_path.is_file():
        raise SystemExit(f"missing resource module: {resource_path.relative_to(ROOT)}")
    tree = ast.parse(resource_path.read_text(encoding="utf-8"))
    actual_operations = {
        (docstring.split(" ", 2)[1], docstring.split(" ", 2)[2][:-1])
        for resource in tree.body
        if isinstance(resource, ast.ClassDef)
        for node in resource.body
        if isinstance(node, ast.FunctionDef)
        if (docstring := ast.get_docstring(node)) is not None
        and docstring.startswith("Call ")
    }
    expected_operations = {(item["method"], item["path"]) for item in operations}
    missing = expected_operations - actual_operations
    unexpected = actual_operations - expected_operations
    if missing or unexpected or len(expected_operations) != len(operations):
        raise SystemExit(
            f"resource mismatch for {domain}: "
            f"missing={sorted(missing)}, unexpected={sorted(unexpected)}"
        )
    expected_count += len(expected_operations)

for obsolete_package in ("services", "utils"):
    if (ROOT / "frontal_sdk" / obsolete_package).exists():
        raise SystemExit(
            f"obsolete frontal_sdk/{obsolete_package} package still exists"
        )

print(
    f"validated {len(FILES)} contract snapshots and {expected_count} resource methods"
)

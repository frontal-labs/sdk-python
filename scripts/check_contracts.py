#!/usr/bin/env python3
"""Validate hand-written resources and report OpenAPI snapshot conformance."""

from __future__ import annotations

import ast
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "contracts/sdk-endpoints.json"
COVERAGE_FLOOR_PATH = ROOT / "contracts/coverage-floor.json"
API_OPENAPI_PATH = ROOT / "contracts/openapi/api.openapi.json"
AI_OPENAPI_PATH = ROOT / "contracts/openapi/ai.openapi.generated.json"
MANIFEST_PATH = ROOT / "contracts/openapi/manifest.json"
FILES = [
    INVENTORY_PATH,
    COVERAGE_FLOOR_PATH,
    API_OPENAPI_PATH,
    AI_OPENAPI_PATH,
    MANIFEST_PATH,
]
HTTP_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE"}
METHOD_ALIASES = {
    "GETRAW": "GET",
    "STREAM": "GET",
    "POSTRAW": "POST",
    "POSTFORMDATA": "POST",
}


def load_json(path: Path) -> Any:
    if not path.is_file():
        raise SystemExit(f"missing contract file: {path.relative_to(ROOT)}")
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def operation_calls(function: ast.FunctionDef) -> set[tuple[str, str]]:
    """Read the actual Operation descriptors from one service method."""
    result: set[tuple[str, str]] = set()
    for node in ast.walk(function):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Name) or node.func.id != "Operation":
            continue
        if len(node.args) < 2:
            continue
        method, path = node.args[:2]
        if (
            isinstance(method, ast.Constant)
            and isinstance(method.value, str)
            and isinstance(path, ast.Constant)
            and isinstance(path.value, str)
        ):
            result.add((method.value, path.value))
    return result


def documented_operation(function: ast.FunctionDef) -> tuple[str, str] | None:
    docstring = ast.get_docstring(function)
    if docstring is None or not docstring.startswith("Call "):
        return None
    parts = docstring.split(" ", 2)
    if len(parts) != 3 or not parts[2].endswith("."):
        return None
    return parts[1], parts[2][:-1]


def class_operations(
    path: Path, resource: ast.ClassDef
) -> tuple[set[tuple[str, str]], list[str]]:
    operations: set[tuple[str, str]] = set()
    errors: list[str] = []
    for function in resource.body:
        if not isinstance(function, ast.FunctionDef):
            continue
        documented = documented_operation(function)
        if documented is None:
            continue
        if "by_param_" in function.name or any(
            re.fullmatch(r"param_\d+", argument.arg) for argument in function.args.args
        ):
            errors.append(
                f"{path.relative_to(ROOT)}:{function.name} uses a generic "
                "path parameter name"
            )
        actual = operation_calls(function)
        if len(actual) != 1:
            errors.append(
                f"{path.relative_to(ROOT)}:{function.name} must call exactly "
                "one Operation descriptor"
            )
            continue
        operation = next(iter(actual))
        if operation != documented:
            errors.append(
                f"{path.relative_to(ROOT)}:{function.name} documents "
                f"{documented} but calls {operation}"
            )
        operations.add(operation)
    return operations, errors


def resource_operations(path: Path) -> tuple[set[tuple[str, str]], list[str]]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    operations: set[tuple[str, str]] = set()
    errors: list[str] = []
    for resource in tree.body:
        if not isinstance(resource, ast.ClassDef):
            continue
        resource_ops, resource_errors = class_operations(path, resource)
        operations.update(resource_ops)
        errors.extend(resource_errors)
    return operations, errors


def resource_endpoint_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return {
        function.name
        for resource in tree.body
        if isinstance(resource, ast.ClassDef)
        for function in resource.body
        if isinstance(function, ast.FunctionDef)
        and documented_operation(function) is not None
    }


def resource_public_method_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return {
        function.name
        for resource in tree.body
        if isinstance(resource, ast.ClassDef)
        for function in resource.body
        if isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef))
        and not function.name.startswith("_")
    }


def parse_openapi(path: Path) -> set[tuple[str, str]]:
    document = load_json(path)
    paths = document.get("paths")
    if not isinstance(paths, dict):
        raise SystemExit(f"OpenAPI file has no paths object: {path.relative_to(ROOT)}")
    operations: set[tuple[str, str]] = set()
    for route, methods in paths.items():
        if not isinstance(route, str) or not isinstance(methods, dict):
            continue
        for method in methods:
            normalized_method = str(method).upper()
            if normalized_method in HTTP_METHODS:
                operations.add((normalized_method, route))
    return operations


def resolve_method(method: str) -> str:
    return METHOD_ALIASES.get(method, method)


def candidate_paths(surface: str, path: str) -> tuple[str, ...]:
    if surface == "api":
        if path.startswith("/v1/"):
            return (path,)
        return (f"/v1{path}", path)
    if path.startswith("/v1/"):
        return (path, re.sub(r"^/v1", "", path, count=1))
    return (path, f"/v1{path}")


def path_matches(spec_path: str, sdk_path: str) -> bool:
    spec_parts = [part for part in spec_path.split("/") if part]
    sdk_parts = [part for part in sdk_path.split("/") if part]
    if len(spec_parts) != len(sdk_parts):
        return False
    for spec_part, sdk_part in zip(spec_parts, sdk_parts):
        spec_param = spec_part.startswith("{") and spec_part.endswith("}")
        sdk_param = sdk_part.startswith("{") and sdk_part.endswith("}")
        if spec_part != sdk_part and not spec_param and not sdk_param:
            return False
    return True


def surface_allows(surface: str, path: str) -> bool:
    if surface == "ai":
        return path == "/health" or path.startswith(("/ai/", "/internal/"))
    return not path.startswith(("/ai/", "/internal/"))


def matches_operation(
    operation: tuple[str, str],
    sdk_operations: list[tuple[str, tuple[str, ...]]],
) -> bool:
    method, path = operation
    return any(
        method == sdk_method
        and any(path_matches(path, candidate) for candidate in paths)
        for sdk_method, paths in sdk_operations
    )


def main() -> None:
    for path in FILES:
        load_json(path)

    inventory = load_json(INVENTORY_PATH)
    coverage_floor = load_json(COVERAGE_FLOOR_PATH)
    if not isinstance(inventory, dict):
        raise SystemExit("endpoint inventory must be a JSON object")
    for surface in ("api", "ai"):
        value = coverage_floor.get(surface)
        if not isinstance(value, int) or value < 0:
            raise SystemExit(
                f"coverage floor must contain a non-negative {surface} count"
            )

    specs = {
        "api": parse_openapi(API_OPENAPI_PATH),
        "ai": parse_openapi(AI_OPENAPI_PATH),
    }
    sdk_by_surface: dict[str, list[tuple[str, tuple[str, ...]]]] = defaultdict(list)
    errors: list[str] = []
    missing_from_spec: list[tuple[str, str, str]] = []
    expected_count = 0

    for domain, entries in inventory.items():
        if not isinstance(domain, str) or not isinstance(entries, list):
            errors.append(f"invalid endpoint inventory entry: {domain!r}")
            continue
        resource_path = ROOT / "frontal_sdk/resources" / f"{domain}.py"
        if not entries:
            if resource_path.exists():
                errors.append(f"unexpected resource module for empty domain: {domain}")
            continue
        if not resource_path.is_file():
            errors.append(f"missing resource module: {resource_path.relative_to(ROOT)}")
            continue

        implemented, resource_errors = resource_operations(resource_path)
        errors.extend(resource_errors)
        expected: set[tuple[str, str]] = set()
        surface = "ai" if domain == "ai" else "api"
        for entry in entries:
            if not isinstance(entry, dict):
                errors.append(f"invalid operation in {domain}: {entry!r}")
                continue
            method, path = entry.get("method"), entry.get("path")
            if not isinstance(method, str) or not isinstance(path, str):
                errors.append(f"invalid method/path in {domain}: {entry!r}")
                continue
            expected.add((method, path))
            resolved_method = resolve_method(method)
            if not surface_allows(surface, path):
                errors.append(
                    f"forbidden {surface} surface operation: {domain} {method} {path}"
                )
            sdk_candidates = candidate_paths(surface, path)
            sdk_by_surface[surface].append((resolved_method, sdk_candidates))
            if not any(
                resolved_method == spec_method
                and any(
                    path_matches(spec_path, candidate) for candidate in sdk_candidates
                )
                for spec_method, spec_path in specs[surface]
            ):
                missing_from_spec.append((domain, method, path))

        if len(expected) != len(entries):
            errors.append(f"duplicate operations in {domain} endpoint inventory")
        missing = expected - implemented
        unexpected = implemented - expected
        if missing or unexpected:
            errors.append(
                f"resource mismatch for {domain}: missing={sorted(missing)}, "
                f"unexpected={sorted(unexpected)}"
            )
        expected_count += len(expected)

    for obsolete_package in ("services", "utils"):
        if (ROOT / "frontal_sdk" / obsolete_package).exists():
            errors.append(
                f"obsolete frontal_sdk/{obsolete_package} package still exists"
            )

    coverage: dict[str, tuple[int, int]] = {}
    uncovered_spec: dict[str, list[tuple[str, str]]] = {}
    for surface, operations in specs.items():
        uncovered = [
            operation
            for operation in sorted(operations)
            if not matches_operation(operation, sdk_by_surface[surface])
        ]
        coverage[surface] = (len(operations) - len(uncovered), len(operations))
        uncovered_spec[surface] = uncovered

    if errors:
        raise SystemExit("\n".join(errors))

    api_covered, api_total = coverage["api"]
    ai_covered, ai_total = coverage["ai"]
    print(
        f"validated {len(FILES)} contract snapshots, {expected_count} "
        f"hand-written resource methods, and OpenAPI surfaces "
        f"(api {api_covered}/{api_total}, ai {ai_covered}/{ai_total})"
    )
    if missing_from_spec:
        print(
            f"OpenAPI baseline drift: {len(missing_from_spec)} inventory "
            "operations are absent from the published snapshots"
        )
    if uncovered_spec["api"] or uncovered_spec["ai"]:
        print(
            "OpenAPI operations not exposed by the endpoint inventory: "
            f"api {len(uncovered_spec['api'])}, ai {len(uncovered_spec['ai'])}"
        )
    for surface, actual in coverage.items():
        floor = coverage_floor[surface]
        if actual[0] < floor:
            print(
                f"OpenAPI coverage floor drift for {surface}: "
                f"{actual[0]} matched, previous floor {floor}"
            )


if __name__ == "__main__":
    main()

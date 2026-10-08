"""Generate typed resource methods from the committed SDK endpoint inventory."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from urllib.parse import parse_qsl

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "contracts" / "sdk-endpoints.json"
OUTPUT = ROOT / "frontal_sdk" / "resources"
VERBS = {
    "GET": "get",
    "GETRAW": "download",
    "POST": "post",
    "PUT": "put",
    "PATCH": "patch",
    "DELETE": "delete",
    "STREAM": "stream",
    "POSTFORMDATA": "upload",
    "POSTRAW": "post_raw",
}


def method_name(method: str, path: str) -> str:
    parts: list[str] = []
    parameter_index = 0
    route, _, fixed_query = path.partition("?")
    for segment in route.strip("/").split("/"):
        if segment.startswith("{") and segment.endswith("}"):
            parameter_index += 1
            parts.extend(("by", f"param_{parameter_index}"))
        else:
            parts.extend(part for part in re.split(r"[-_]", segment) if part)
    for key, value in parse_qsl(fixed_query, keep_blank_values=True):
        parts.extend(("query", *re.findall(r"[A-Za-z0-9]+", key)))
        parts.extend(re.findall(r"[A-Za-z0-9]+", value))
    return "_".join((VERBS[method], *parts))


def method_source(method: str, path: str, name: str) -> str:
    placeholders = re.findall(r"\{[^{}]+\}", path.partition("?")[0])
    params = [f"param_{index}: str" for index in range(1, len(placeholders) + 1)]
    path_values = [f"param_{index}" for index in range(1, len(params) + 1)]
    path_tuple = f"({', '.join(path_values)}{',' if len(path_values) == 1 else ''})"
    if not path_values:
        path_tuple = "()"
    query_arg = "query: QueryParams | None = None"
    signature_args = [*params, "*", query_arg]
    if method in {"POST", "PUT", "PATCH"}:
        signature_args.append("body: JSONValue = None")
    if method == "GETRAW":
        return_type = "bytes"
        call = (
            "self._request_bytes(\n"
            f"            Operation({method!r}, {path!r}),\n"
            f"            path_params={path_tuple},\n"
            "            query=query,\n"
            "        )"
        )
    elif method == "STREAM":
        return_type = "Iterator[ServerEvent]"
        call = (
            "self._stream(\n"
            f"            Operation({method!r}, {path!r}),\n"
            f"            path_params={path_tuple},\n"
            "            query=query,\n"
            "        )"
        )
    elif method == "POSTRAW":
        return_type = "bytes"
        signature_args = [
            *params,
            "data: bytes",
            "content_type: str",
            "*",
            query_arg,
        ]
        call = (
            "self._post_raw(\n"
            f"            Operation({method!r}, {path!r}),\n"
            "            data,\n"
            "            content_type,\n"
            f"            path_params={path_tuple},\n"
            "            query=query,\n"
            "        )"
        )
    elif method == "POSTFORMDATA":
        return_type = "JSONValue"
        signature_args = [
            *params,
            "parts: Sequence[MultipartPart]",
            "*",
            "fields: Mapping[str, str] | None = None",
        ]
        call = (
            "self._upload(\n"
            f"            Operation({method!r}, {path!r}),\n"
            "            parts,\n"
            f"            path_params={path_tuple},\n"
            "            fields=fields,\n"
            "        )"
        )
    else:
        return_type = "JSONValue"
        body_argument = ", body=body" if method in {"POST", "PUT", "PATCH"} else ""
        call = (
            "self._request(\n"
            f"            Operation({method!r}, {path!r}),\n"
            f"            path_params={path_tuple},\n"
            f"            query=query{body_argument},\n"
            "        )"
        )
    signature = (
        f"    def {name}(\n        self,\n        "
        + ",\n        ".join(signature_args)
        + f"\n    ) -> {return_type}:"
    )
    lines = [signature]
    lines.extend([f'        """Call {method} {path}."""', f"        return {call}", ""])
    return "\n".join(lines)


def generate() -> None:
    catalog: dict[str, list[dict[str, str]]] = json.loads(
        INVENTORY.read_text(encoding="utf-8")
    )
    OUTPUT.mkdir(parents=True, exist_ok=True)
    resource_classes: list[tuple[str, str]] = []
    generated_domains: set[str] = set()
    for domain, operations in catalog.items():
        if not operations:
            continue
        generated_domains.add(domain)
        class_name = (
            "AI"
            if domain == "ai"
            else "".join(part.title() for part in domain.split("_"))
        )
        resource_classes.append((domain, class_name))
        methods: list[str] = []
        seen: set[str] = set()
        for operation in operations:
            method, path = operation["method"], operation["path"]
            name = method_name(method, path)
            if name in seen:
                raise ValueError(f"duplicate resource method {domain}.{name}")
            seen.add(name)
            methods.append(method_source(method, path, name))
        collection_imports: set[str] = set()
        return_imports: set[str] = set()
        if any(operation["method"] == "STREAM" for operation in operations):
            collection_imports.add("Iterator")
            return_imports.add("ServerEvent")
        if any(operation["method"] == "POSTFORMDATA" for operation in operations):
            collection_imports.update(("Mapping", "Sequence"))
            return_imports.add("MultipartPart")
        model_imports = sorted({"JSONValue", "QueryParams", *return_imports})
        source = [
            f'"""Typed API resource for the {domain} endpoints.\n\n'
            "Generated by ``scripts/generate_resources.py``.\n\n"
            '"""',
            "",
            "from __future__ import annotations",
            "",
        ]
        if collection_imports:
            source.append(
                f"from collections.abc import {', '.join(sorted(collection_imports))}"
            )
            source.append("")
        source.extend(
            [
                "from frontal_sdk.core.operation import Operation",
                f"from frontal_sdk.models import {', '.join(model_imports)}",
                "from frontal_sdk.resources._base import APIResource",
                "",
                "",
                f"class {class_name}(APIResource):",
                f'    """Methods for the {domain} API endpoints."""',
                "",
                *methods,
            ]
        )
        (OUTPUT / f"{domain}.py").write_text(
            "\n".join(source).rstrip() + "\n", encoding="utf-8"
        )
    for resource_path in OUTPUT.glob("*.py"):
        if (
            not resource_path.stem.startswith("_")
            and resource_path.stem not in generated_domains
        ):
            resource_path.unlink()
    init = [
        '"""Typed API resources exposed by :class:`frontal_sdk.Frontal`."""',
        "",
        *[
            f"from frontal_sdk.resources.{domain} import {name}"
            for domain, name in resource_classes
        ],
        "",
        "__all__ = [",
        *[f'    "{name}",' for _, name in resource_classes],
        "]",
        "",
    ]
    (OUTPUT / "__init__.py").write_text("\n".join(init), encoding="utf-8")
    subprocess.run(["ruff", "format", str(OUTPUT)], check=True)


if __name__ == "__main__":
    generate()

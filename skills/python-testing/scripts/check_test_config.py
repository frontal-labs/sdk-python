#!/usr/bin/env python3
"""Read-only audit of pytest/coverage configuration in a Python package repo.

Finds the misconfigurations that make test infrastructure lie: shadowed or
split config sources, a config table the installed tools silently ignore,
missing branch coverage, and coverage gates that were never wired up.

This script only READS files. It never modifies the repo, never runs the test
suite, and never installs anything. Version checks that require executing tools
(e.g. `pytest --version`) are intentionally left to the caller.

Usage:
    python3 check_test_config.py [--root PATH] [--strict]

Output: one machine-readable line per finding:
    ERROR <file>: <message>
    WARN  <file>: <message>
    INFO  <file>: <message>

Exit codes: 0 = no errors (warnings allowed unless --strict), 1 = errors found.

Requires Python 3.11+ for full TOML-aware checks (stdlib tomllib); on 3.10 it
falls back to section-presence checks only and says so.
"""

# Keep full, actionable testing guidance in this standalone checker.
# ruff: noqa: E501

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import tomllib
except ImportError:  # Python 3.10: degrade to text-level checks
    tomllib = None

errors: list[str] = []
warnings: list[str] = []
infos: list[str] = []


def err(where: str, msg: str) -> None:
    errors.append(f"ERROR {where}: {msg}")


def warn(where: str, msg: str) -> None:
    warnings.append(f"WARN  {where}: {msg}")


def info(where: str, msg: str) -> None:
    infos.append(f"INFO  {where}: {msg}")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        err(str(path), f"cannot read: {exc}")
        return ""


def has_section(text: str, section: str) -> bool:
    """Text-level TOML/INI section presence check, e.g. section='tool.pytest'."""
    pattern = re.compile(
        r"^\s*\[" + re.escape(section) + r"(\.[A-Za-z0-9_.-]+)?\]", re.M
    )
    return bool(pattern.search(text))


def has_exact_section(text: str, section: str) -> bool:
    pattern = re.compile(r"^\s*\[" + re.escape(section) + r"\]", re.M)
    return bool(pattern.search(text))


def addopts_as_string(value: object) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(str(v) for v in value)
    return ""


def pytest_table_flags(pp_text: str, tool: dict) -> tuple[bool, bool, bool]:
    pytest_table = tool.get("pytest")
    if tomllib is not None and pp_text:
        has_ini = isinstance(pytest_table, dict) and "ini_options" in pytest_table
        has_native = isinstance(pytest_table, dict) and any(
            key != "ini_options" for key in pytest_table
        )
        has_coverage = "coverage" in tool
        return has_ini, has_native, has_coverage
    return (
        has_exact_section(pp_text, "tool.pytest.ini_options"),
        has_exact_section(pp_text, "tool.pytest"),
        has_section(pp_text, "tool.coverage"),
    )


def check_conflicting_sources(
    pytest_ini: Path,
    toml_configs: list[Path],
    setup_cfg: Path,
    tox_ini: Path,
    has_pytest: bool,
    setup_has_pytest: bool,
    tox_has_pytest: bool,
) -> None:
    if pytest_ini.is_file() and has_pytest:
        err(
            str(pytest_ini),
            "pytest.ini exists alongside pytest config in pyproject.toml — pytest.ini silently wins; merge into one source and delete the other",
        )
    if has_pytest or pytest_ini.is_file():
        for cfg in toml_configs:
            err(
                str(cfg),
                f"{cfg.name} exists alongside other pytest config — it takes precedence over every other file, even when empty; keep exactly one source",
            )
    if setup_has_pytest and has_pytest:
        warn(
            str(setup_cfg),
            "[tool:pytest] in setup.cfg alongside pytest config in pyproject.toml — only one source is read; merge and delete the loser",
        )
    if tox_has_pytest and has_pytest:
        warn(
            str(tox_ini),
            "[pytest] section in tox.ini alongside pytest config in pyproject.toml — only one source is read; merge and delete the loser",
        )


def check_pytest_table_compatibility(
    pyproject: Path, has_ini: bool, has_native: bool
) -> None:
    if has_native and has_ini:
        err(
            str(pyproject),
            "both [tool.pytest] and [tool.pytest.ini_options] present — pytest reads one table; merge into the one your pytest major supports",
        )
    elif has_native:
        info(
            str(pyproject),
            "[tool.pytest] native table (pytest >= 9.0) — SILENTLY ignored on older pytest; confirm with `pytest --version`, or use [tool.pytest.ini_options] if < 9 must work",
        )


def warn_missing_pytest_config(
    root: Path,
    has_pytest: bool,
    pytest_ini: Path,
    toml_configs: list[Path],
    setup_has_pytest: bool,
    tox_has_pytest: bool,
) -> None:
    sources_exist = has_pytest or pytest_ini.is_file() or toml_configs
    if not (sources_exist or setup_has_pytest or tox_has_pytest):
        warn(
            str(root),
            "no pytest configuration found in pyproject.toml, pytest.toml, pytest.ini, setup.cfg, or tox.ini — add [tool.pytest.ini_options] (or [tool.pytest] on pytest >= 9) with testpaths and strict flags",
        )


def check_config_sources(
    root: Path,
    pyproject: Path,
    pytest_ini: Path,
    toml_configs: list[Path],
    setup_cfg: Path,
    tox_ini: Path,
    has_ini: bool,
    has_native: bool,
) -> None:
    has_pytest = has_ini or has_native
    setup_cfg_text = read_text(setup_cfg) if setup_cfg.is_file() else ""
    tox_ini_text = read_text(tox_ini) if tox_ini.is_file() else ""
    setup_has_pytest = bool(setup_cfg_text) and has_exact_section(
        setup_cfg_text, "tool:pytest"
    )
    tox_has_pytest = bool(tox_ini_text) and has_exact_section(tox_ini_text, "pytest")
    check_conflicting_sources(
        pytest_ini,
        toml_configs,
        setup_cfg,
        tox_ini,
        has_pytest,
        setup_has_pytest,
        tox_has_pytest,
    )
    check_pytest_table_compatibility(pyproject, has_ini, has_native)
    warn_missing_pytest_config(
        root,
        has_pytest,
        pytest_ini,
        toml_configs,
        setup_has_pytest,
        tox_has_pytest,
    )


def check_coverage_config(
    pyproject: Path,
    coveragerc: Path,
    tool: dict,
    has_coverage: bool,
    pytest_table: object,
) -> None:
    if coveragerc.is_file() and has_coverage:
        err(
            str(coveragerc),
            ".coveragerc exists alongside [tool.coverage.*] in pyproject.toml — .coveragerc silently wins; keep exactly one source",
        )
    if (
        tomllib is None
        or not has_coverage
        or not isinstance(tool.get("coverage"), dict)
    ):
        return

    coverage = tool["coverage"]
    run = coverage.get("run", {}) if isinstance(coverage.get("run", {}), dict) else {}
    report = (
        coverage.get("report", {})
        if isinstance(coverage.get("report", {}), dict)
        else {}
    )
    if run.get("branch") is not True:
        warn(
            str(pyproject),
            "[tool.coverage.run] branch is not true — line-only coverage overstates; set branch = true",
        )
    if run.get("parallel") is True and run.get("relative_files") is not True:
        warn(
            str(pyproject),
            "[tool.coverage.run] parallel = true without relative_files = true — combining data across paths/runners will mismatch files",
        )

    ini = pytest_table.get("ini_options", {}) if isinstance(pytest_table, dict) else {}
    addopts = addopts_as_string(ini.get("addopts", "")) if isinstance(ini, dict) else ""
    if "fail_under" not in report and "--cov-fail-under" not in addopts:
        warn(
            str(pyproject),
            "no coverage gate found — set fail_under under [tool.coverage.report] (80-90), then prove it trips with a non-zero exit",
        )
    if "--cov" in addopts.split() or "--cov=" in addopts:
        info(
            str(pyproject),
            "--cov baked into pytest addopts — every run (incl. single-test debugging) pays coverage overhead; --no-cov disables per run",
        )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--root", type=Path, default=Path.cwd(), help="package repo root (default: cwd)"
    )
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = ap.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        err(str(root), "not a directory")
        print(errors[0], file=sys.stderr)
        print("FAIL: 1 error(s), 0 warning(s)")
        return 1

    pyproject = root / "pyproject.toml"
    pytest_ini = root / "pytest.ini"
    toml_configs = [
        p
        for p in (root / "pytest.toml", root / ".pytest.toml", root / ".pytest.ini")
        if p.is_file()
    ]
    setup_cfg = root / "setup.cfg"
    tox_ini = root / "tox.ini"
    coveragerc = root / ".coveragerc"
    pp_text = read_text(pyproject) if pyproject.is_file() else ""
    pp_data: dict = {}
    if pp_text and tomllib is not None:
        try:
            pp_data = tomllib.loads(pp_text)
        except tomllib.TOMLDecodeError as exc:
            err(str(pyproject), f"invalid TOML: {exc}")
    elif pp_text and tomllib is None:
        info(
            str(pyproject),
            "Python < 3.11 (no tomllib) — key-level checks skipped, section-presence checks only",
        )

    raw_tool = pp_data.get("tool", {})
    tool = raw_tool if isinstance(raw_tool, dict) else {}
    has_ini, has_native, has_coverage = pytest_table_flags(pp_text, tool)
    check_config_sources(
        root,
        pyproject,
        pytest_ini,
        toml_configs,
        setup_cfg,
        tox_ini,
        has_ini,
        has_native,
    )
    check_coverage_config(pyproject, coveragerc, tool, has_coverage, tool.get("pytest"))

    for line in errors + warnings + infos:
        print(line, file=sys.stderr)
    n_fail = len(errors) + (len(warnings) if args.strict else 0)
    print(
        f"{'FAIL' if n_fail else 'OK'}: {len(errors)} error(s), {len(warnings)} warning(s), {len(infos)} info"
    )
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())

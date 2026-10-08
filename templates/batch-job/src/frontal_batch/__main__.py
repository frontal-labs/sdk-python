"""Batch lookup entry point for the Frontal SDK template."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import TextIO

from frontal_sdk import Frontal, FrontalError, JSONValue

logger = logging.getLogger("frontal_batch")


def process_agent_ids(
    agent_ids: Iterable[str], *, output: TextIO, client: Frontal
) -> int:
    """Write one JSON result per agent ID and return the failure count."""
    failures = 0
    for agent_id in agent_ids:
        normalized_id = agent_id.strip()
        if not normalized_id:
            continue
        try:
            result = client.agents.get_agents_by_param_1(normalized_id)
        except FrontalError as error:
            failures += 1
            logger.error("agent lookup failed for %s: %s", normalized_id, error)
            record: dict[str, JSONValue] = {
                "agent_id": normalized_id,
                "ok": False,
                "error": str(error),
            }
        else:
            record = {"agent_id": normalized_id, "ok": True, "data": result}
        output.write(json.dumps(record) + "\n")
    return failures


def main(argv: Sequence[str] | None = None) -> int:
    """Read agent IDs from a text file and emit JSON Lines results."""
    parser = argparse.ArgumentParser(prog="frontal-batch")
    parser.add_argument(
        "input", type=Path, help="text file containing one agent ID per line"
    )
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)

    try:
        with Frontal.from_env() as client:
            with args.input.open(encoding="utf-8") as input_file:
                failures = process_agent_ids(
                    input_file, output=sys.stdout, client=client
                )
    except ValueError as error:
        logger.error("client configuration failed: %s", error)
        return 2
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

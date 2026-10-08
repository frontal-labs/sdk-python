"""Command line entry point for the Frontal SDK template."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence

from frontal_sdk import Frontal, FrontalError


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(prog="frontal-cli")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("health", help="check the AI API health endpoint")
    commands.add_parser("agents", help="list agents")
    get_agent = commands.add_parser("agent", help="get one agent by ID")
    get_agent.add_argument("agent_id")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run one SDK command and print its JSON result."""
    args = build_parser().parse_args(argv)
    try:
        with Frontal.from_env() as client:
            if args.command == "health":
                result = client.ai.health()
            elif args.command == "agents":
                result = client.agents.get_agents()
            else:
                result = client.agents.get_agents_by_param_1(args.agent_id)
    except FrontalError as error:
        print(f"Frontal API request failed: {error}", file=sys.stderr)
        return 1
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

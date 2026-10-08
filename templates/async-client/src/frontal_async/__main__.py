"""Asyncio entry point for the Frontal SDK template."""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
from collections.abc import Sequence

from frontal_sdk import AsyncFrontal, FrontalError, JSONValue

logger = logging.getLogger("frontal_async")


async def fetch_agent(
    client: AsyncFrontal, agent_id: str, semaphore: asyncio.Semaphore
) -> tuple[str, JSONValue | FrontalError]:
    """Run one native asynchronous SDK request."""
    async with semaphore:
        try:
            result = await client.agents.get_agents_by_param_1(agent_id)
        except FrontalError as error:
            return agent_id, error
        return agent_id, result


async def run(agent_ids: Sequence[str], *, concurrency: int) -> int:
    """Fetch agents concurrently and print one JSON result per ID."""
    semaphore = asyncio.Semaphore(concurrency)
    async with AsyncFrontal.from_env() as client:
        results = await asyncio.gather(
            *(fetch_agent(client, agent_id, semaphore) for agent_id in agent_ids)
        )

    failures = 0
    for agent_id, result in results:
        if isinstance(result, FrontalError):
            failures += 1
            logger.error("agent lookup failed for %s: %s", agent_id, result)
            record: dict[str, JSONValue] = {
                "agent_id": agent_id,
                "ok": False,
                "error": str(result),
            }
        else:
            record = {"agent_id": agent_id, "ok": True, "data": result}
        print(json.dumps(record))
    return 1 if failures else 0


def main(argv: Sequence[str] | None = None) -> int:
    """Parse IDs and run the asynchronous SDK client."""
    parser = argparse.ArgumentParser(prog="frontal-async")
    parser.add_argument("agent_ids", nargs="+", help="agent IDs to fetch")
    parser.add_argument(
        "--concurrency", type=int, default=5, help="maximum concurrent requests"
    )
    args = parser.parse_args(argv)
    if args.concurrency < 1:
        parser.error("--concurrency must be positive")
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    try:
        return asyncio.run(run(args.agent_ids, concurrency=args.concurrency))
    except ValueError as error:
        logger.error("client configuration failed: %s", error)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

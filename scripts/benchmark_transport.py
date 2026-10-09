#!/usr/bin/env python3
"""Measure local JSON transport overhead without network variability."""

from __future__ import annotations

import argparse
import asyncio
import time

import httpx
from frontal_sdk import AsyncFrontal, Frontal
from frontal_sdk.core import Operation


def response(request: httpx.Request) -> httpx.Response:
    return httpx.Response(200, json={"ok": True})


def benchmark_sync(iterations: int) -> float:
    http = httpx.Client(transport=httpx.MockTransport(response))
    client = Frontal("frt_benchmark_key", http_client=http, max_retries=0)
    operation = Operation("GET", "/health")
    started = time.perf_counter()
    for _ in range(iterations):
        client._http.request(operation)
    elapsed = time.perf_counter() - started
    http.close()
    return elapsed


async def benchmark_async(iterations: int) -> float:
    http = httpx.AsyncClient(transport=httpx.MockTransport(response))
    client = AsyncFrontal("frt_benchmark_key", http_client=http, max_retries=0)
    operation = Operation("GET", "/health")
    started = time.perf_counter()
    for _ in range(iterations):
        await client._http.request(operation)
    elapsed = time.perf_counter() - started
    await http.aclose()
    return elapsed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iterations", type=int, default=1000)
    arguments = parser.parse_args()
    if arguments.iterations < 1:
        parser.error("--iterations must be positive")

    sync_elapsed = benchmark_sync(arguments.iterations)
    async_elapsed = asyncio.run(benchmark_async(arguments.iterations))
    print(
        f"sync: {arguments.iterations / sync_elapsed:.0f} mocked JSON requests/s "
        f"({sync_elapsed:.3f}s total)"
    )
    print(
        f"async: {arguments.iterations / async_elapsed:.0f} mocked JSON requests/s "
        f"({async_elapsed:.3f}s total)"
    )


if __name__ == "__main__":
    main()

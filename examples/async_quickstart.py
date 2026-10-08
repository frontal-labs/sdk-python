"""Generate text with the native asynchronous Frontal client."""

from __future__ import annotations

import asyncio

from frontal_sdk import AsyncFrontal


async def main() -> None:
    async with AsyncFrontal() as client:
        result = await client.ai.generate_text(
            {"model": "frontal-ai-fast", "prompt": "Say hello."}
        )
        print(result.text)


if __name__ == "__main__":
    asyncio.run(main())

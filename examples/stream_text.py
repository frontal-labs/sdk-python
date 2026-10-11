"""Stream chat text deltas using the Frontal Python SDK."""

from frontal_sdk import Frontal


def main() -> None:
    with Frontal() as client:
        for part in client.ai.stream_text(
            {"model": "frontal-ai-fast", "prompt": "Count to three."}
        ):
            if part.type == "text":
                print(part.text, end="", flush=True)
            elif part.type == "finish":
                print(f"\n[finished: {part.finish_reason}]")
            elif part.type == "error":
                print(f"\n[stream error: {part.error}]")
        # "done" parts terminate the stream; there is nothing to print.


if __name__ == "__main__":
    main()

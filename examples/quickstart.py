"""Generate text using the Frontal Python SDK."""

from frontal_sdk import Frontal


def main() -> None:
    with Frontal() as client:
        result = client.ai.generate_text(
            {"model": "frontal-ai-fast", "prompt": "Say hello."}
        )
        print(result.text)


if __name__ == "__main__":
    main()

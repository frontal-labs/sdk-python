"""Make a health request using the Frontal Python SDK."""

from frontal_sdk import Frontal


def main() -> None:
    with Frontal() as client:
        print(client.ai.get_health())


if __name__ == "__main__":
    main()

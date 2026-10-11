"""Demonstrate structured error handling with the Frontal Python SDK."""

from frontal_sdk import Frontal, FrontalError, RateLimitError, ValidationError


def main() -> None:
    with Frontal() as client:
        try:
            client.agents.list(query={"limit": 50})
        except RateLimitError as error:
            print(f"Rate limited; retry after {error.retry_after}s")
            if error.fix is not None:
                print(f"Hint: {error.fix}")
        except ValidationError as error:
            print(f"Invalid request ({error.code}):")
            for field in error.fields:
                print(f"  - {field.field}: {field.message}")
        except FrontalError as error:
            print(f"Request failed [{error.code}]: {error}")
            if error.fix is not None:
                print(f"Hint: {error.fix}")
            if error.safe_to_retry:
                print("This operation is safe to retry.")


if __name__ == "__main__":
    main()

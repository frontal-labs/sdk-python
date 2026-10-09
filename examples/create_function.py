"""Create a Frontal function and invoke it with JSON input."""

from frontal_sdk import (
    Frontal,
    FunctionInvocationInput,
    FunctionInvocationResult,
    FunctionResource,
)


def main() -> None:
    with Frontal() as client:
        created = (
            client.functions.define("hello-world")
            .runtime("nodejs22")
            .entrypoint("index.handler")
            .description("Return a greeting")
            .input_schema(
                {"type": "object", "properties": {"name": {"type": "string"}}}
            )
            .create()
        )
        function = FunctionResource.model_validate(created)
        raw_result = client.functions.executions.invoke(
            FunctionInvocationInput(
                function_id=function.id,
                input={"name": "World", "metadata": {"source": "example"}},
            )
        )
        result = FunctionInvocationResult.model_validate(raw_result)
        print(result.result)


if __name__ == "__main__":
    main()

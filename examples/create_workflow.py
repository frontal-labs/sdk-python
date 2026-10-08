"""Create a workflow and trigger its first execution."""

from __future__ import annotations

import json

from frontal_sdk import Frontal


def main() -> None:
    with Frontal() as client:
        workflow = (
            client.workflows.define("Support ticket handoff")
            .description("Review a new ticket and route it to the support queue")
            .manual()
            .task("review", {"action": "review_ticket"}, timeout="30s")
            .create()
        )
        workflow_id = str(workflow["id"])
        execution = client.workflows.use(workflow_id).trigger(
            {"ticket_id": "ticket_123"}
        )
    print(json.dumps({"workflow": workflow, "execution": execution}, indent=2))


if __name__ == "__main__":
    main()

"""Create a ticket triage agent with a validated definition builder."""

from __future__ import annotations

import json

from frontal_sdk import Frontal


def main() -> None:
    with Frontal() as client:
        agent = (
            client.agents.define("Ticket triage")
            .description("Route new support tickets")
            .trigger("ticket.created")
            .can_read("tickets")
            .can_write("ticket_assignments")
            .timeout("30s")
            .tags("support")
            .create()
        )
    print(json.dumps(agent, indent=2))


if __name__ == "__main__":
    main()

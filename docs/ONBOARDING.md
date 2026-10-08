# Python onboarding

1. Install Python 3.9–3.12 and `uv`.
2. Clone this repository, then run `uv sync --extra dev` from the root.
3. Run the quality commands in the root README.
4. Review `AGENTS.md`, `docs/ARCHITECTURE.md`, and `contracts/README.md`.
5. Compare service methods with `contracts/sdk-endpoints.json` before adding or
   changing a public operation.
6. Choose a starter project under `templates/` for a CLI, batch job, or async
   application.

`Frontal()` and `AsyncFrontal()` read the `FRONTAL_*` variables from the
process environment. Python does not load `.env` files automatically. Tests
use RESPX mocks and do not need a key or a live service.

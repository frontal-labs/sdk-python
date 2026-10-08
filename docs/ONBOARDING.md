# Python onboarding

1. Install Python 3.10 or later.
2. Clone this repository, create a virtual environment, and install the development extra with `python -m pip install -e ".[dev]"`.
3. Run the format, lint, type-check, test, and build commands in the root README.
4. Review `AGENTS.md`, `docs/ARCHITECTURE.md`, and `contracts/README.md`.
5. Select a service module and compare its planned operations with `contracts/sdk-endpoints.json`.
6. Add implementation, Python tests, documentation, and examples together.

Run the quality commands in the root README after making changes. `Frontal.from_env()` reads process environment variables; Python does not load `.env` files automatically.

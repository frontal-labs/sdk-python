# Python testing strategy

Tests live under the repository-level `tests/` directory and are not included in the SDK distribution. The current suite exercises request encoding, authentication, endpoint path handling, retries, structured errors, uploads, raw responses, and event streams against a local HTTP server.

Run the suite with `python -m pytest`. Keep tests independent of Frontal credentials and avoid live API calls in the default run. Organize new test modules by service or shared runtime area as the suite grows.

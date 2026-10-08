# Contributing to the Frontal Python SDK

## Set up

Install Python 3.9–3.12 and `uv`. Follow [`docs/ONBOARDING.md`](./docs/ONBOARDING.md) to prepare the Python toolchain and local environment.

## Make a change

- Put shared transport and error behavior in `core`.
- Put each service's methods in its corresponding `frontal_sdk/resources/` module.
- Keep the unified clients in `frontal_sdk/client.py`, tests in root `tests/`, and Markdown guidance in `docs/`.
- Use `uv`, Ruff, mypy, pytest, and Hatchling as configured in `pyproject.toml`.
- Keep contracts and conformance reports synchronized when public endpoint coverage changes.
- Add API documentation and a runnable Python example for each public operation.
- Use Conventional Commits (`type(scope): summary`); pull request titles are checked for this format and drive release notes.
- Write clear Conventional Commit pull request titles; Release Please composes `CHANGELOG.md` from merged titles.

## Before opening a pull request

Run the commands in the root README and report any contract or public API changes. Do not include live credentials in tests or examples. Release Please opens a version and changelog pull request after qualifying commits reach `main`; merge it after CI passes to create the tag and GitHub release.

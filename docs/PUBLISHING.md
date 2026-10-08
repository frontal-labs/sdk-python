# Publishing to PyPI

Build the wheel and source distribution with `uv build`. The `publish.yml`
workflow publishes the `frontal` distribution to PyPI when a `v*.*.*` tag is
pushed. It uses GitHub Actions OIDC through `pypa/gh-action-pypi-publish`; no
PyPI API token is stored in the repository.

Before the first release, configure PyPI Trusted Publishing for owner
`frontal-labs`, repository `sdk-python`, workflow `publish.yml`, and the GitHub
environment `pypi`. Protect that environment with the repository's release
review rules. A release tag must match the package version in `pyproject.toml`;
the first tag is `v1.0.0`.

The release workflow runs formatting, build, lint, strict typing, offline tests,
and the contract gate before uploading. Release notes are collected with
Towncrier fragments in `changelog.d/` and included in `CHANGELOG.md`.

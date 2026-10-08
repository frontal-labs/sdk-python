# Publishing to PyPI

Build the wheel and source distribution with `uv build`. The `publish.yml`
workflow publishes the `frontal` distribution to PyPI when Release Please creates a
`v*.*.*` tag. It uses GitHub Actions OIDC through
`pypa/gh-action-pypi-publish`; no PyPI API token is stored in the repository.

Before the first release, configure a fine-grained repository secret named
`RELEASE_PLEASE_TOKEN` with contents and pull request write access. Release
Please uses it to create release pull requests and tags that trigger the
publishing workflow. Configure PyPI Trusted Publishing for owner
`frontal-labs`, repository `sdk-python`, workflow `publish.yml`, and the GitHub
environment `pypi`. Protect that environment with the repository's release
review rules. A release tag must match the package version in `pyproject.toml`;
the first tag is `v1.0.0`.

The release workflow runs formatting, build, lint, strict typing, offline tests,
and the contract gate before uploading, and creates a provenance attestation for
the distributions. Release Please generates `CHANGELOG.md` from Conventional
Commits in its release pull request.

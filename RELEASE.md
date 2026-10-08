# Releasing the Frontal Python SDK

Build both distributions with `uv build`. Publish `frontal` to PyPI by pushing
the matching version tag, using the GitHub Actions OIDC workflow in
`.github/workflows/publish.yml`. Configure the PyPI trusted publisher for
`frontal-labs/sdk-python`, workflow `publish.yml`, and environment `pypi` before
the first release. The first tag is `v1.0.0`.

Before release, update `CHANGELOG.md`, confirm the supported Python version range, regenerate resources and the contract matrix, and verify package metadata. Publishing automation is configured in `.github/workflows/publish.yml`.

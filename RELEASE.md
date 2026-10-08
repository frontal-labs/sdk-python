# Releasing the Frontal Python SDK

Build both wheel and source distributions with `python -m build`. Publish `frontal-sdk` to PyPI using a protected version tag and GitHub trusted publishing (OIDC). Verify the uploaded metadata, files, and release notes on PyPI.

Before release, update `CHANGELOG.md`, confirm the supported Python version range, check the generated contract matrix, and verify package metadata. Publishing automation is not enabled while this repository is a scaffold.

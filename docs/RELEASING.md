# Python release checklist

For a release, update `pyproject.toml` and `frontal_sdk.__version__`, add a
Towncrier fragment under `changelog.d/`, render the changelog, and confirm all
CI gates pass. Push the matching version tag (for example `v1.0.0`); the
`publish.yml` workflow validates the package and publishes `frontal` to PyPI
using OIDC trusted publishing. Verify the uploaded metadata, wheel, source
distribution, and release notes on PyPI.

Before publishing, run the Python CI checks, update the changelog and package metadata, review `contracts/reports/migration-matrix.md`, and verify the artifact contents.

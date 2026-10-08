# Python release checklist

Build both wheel and source distributions with `python -m build`. Publish `frontal-sdk` to PyPI using a protected version tag and GitHub trusted publishing (OIDC). Verify the uploaded metadata, files, and release notes on PyPI.

Before publishing, run the Python CI checks, update the changelog and package metadata, review `contracts/reports/migration-matrix.md`, and verify the artifact contents.

# Publishing to PyPI

Build both wheel and source distributions with `python -m build`. Publish `frontal-sdk` to PyPI using a protected version tag and GitHub trusted publishing (OIDC). Verify the uploaded metadata, files, and release notes on PyPI.

The repository currently has no registry publishing credentials or release action. Complete the implementation and release metadata first. Keep credentials in protected repository secrets and use the registry's recommended signing or trusted-publishing mechanism where available.

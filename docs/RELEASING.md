# Python release process

Use Conventional Commit pull request titles (for example,
`feat(client): add retry option`). After those commits reach `main`, Release
Please opens or updates a release pull request with the version bump and
generated `CHANGELOG.md`. Review the release notes and package version fields,
then merge the release pull request only after all required CI checks pass.

The merge creates the version tag and GitHub Release. The `publish.yml`
workflow reruns the package quality and contract checks, generates provenance
for the wheel and source distribution, then publishes `frontal` to PyPI through
OIDC. The `pypi` environment must have required reviewers configured. Verify
the uploaded metadata and files on PyPI after publication.

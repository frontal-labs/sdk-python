# Enterprise readiness

The Python SDK includes sync and async HTTPX transports, validated client configuration, structured API errors, bounded GET retries, Pydantic boundary models, and methods for the complete endpoint inventory. The repository also contains a GitHub OIDC PyPI publishing workflow with SBOM generation and build provenance attestation. Remaining readiness work is:

- Obtain verified operation-specific request and response schemas from API owners. The committed API snapshot has no request-body schemas and uses generic object schemas for successful responses; the AI snapshot has no operation response schemas.
- Configure the PyPI trusted publisher for this repository, the `publish.yml` workflow, and the `pypi` environment in the PyPI project settings.
- Review security controls, supported authentication flows, and service-specific operational guidance during release review.

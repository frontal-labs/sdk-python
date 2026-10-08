# Branch protection baseline

# Recommended ruleset for `main`

In **Settings → Rules → Rulesets**, create an active branch ruleset targeting the
default branch (`main`) with these settings:

- Require a pull request before merging, with at least one approval.
- Require approval of the most recent push and dismiss stale approvals after
  new commits; require all review conversations to be resolved.
- Require these CI checks: `Python 3.9 (ubuntu-latest)`,
  `Python 3.10 (ubuntu-latest)`, `Python 3.11 (ubuntu-latest)`,
  `Python 3.12 (ubuntu-latest)`, `Python 3.12 (macos-latest)`, and
  `Python 3.12 (windows-latest)`.
- Require the `CodeQL / analyze` and `Dependency review` checks.
- Require linear history. Block force pushes and branch deletion.
- Allow squash merges only and use the pull request title as the squash commit
  message so the Conventional Commit check matches Release Please's history.
- Do not allow bypassing these rules except for a documented emergency
  administrator role.

Also create a tag ruleset for `v*` that blocks tag deletion and updates. Configure
the `pypi` environment under **Settings → Environments** with required reviewers
and prevent self-review. These controls cannot be committed as repository files.

Under **Settings → Code security and analysis**, enable the dependency graph,
Dependabot alerts, Dependabot security updates, secret scanning, and push
protection where available. Enable private vulnerability reporting for the
repository. On plans that do not provide secret scanning, use an organization
or third-party scanner and retain push protection through that service.

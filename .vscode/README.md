# VS Code workspace setup

This folder contains portable workspace settings, extension recommendations, and manually invoked tasks. Open the repository root as a folder in VS Code; no machine-specific paths are configured. Tasks do not run automatically.

Python testing is configured for pytest in tests/. The formatter and import actions use Ruff. Select the project interpreter with “Python: Select Interpreter”; no local interpreter path is hard-coded.

The repository's `.editorconfig` remains authoritative for whitespace and line endings. See `AGENTS.md` for the full development workflow.

# Python repository scripts

`check_contracts.py` validates the committed API snapshots, endpoint inventory,
and hand-written service methods. `generate_docs_manifest.py` indexes Markdown
documentation and writes `docs/mcp.json` plus the root `mcp.json`. Both are
repository maintenance utilities written in Python 3's standard library; they
do not affect the SDK runtime or package dependencies.

Run them directly:

```bash
python scripts/check_contracts.py
python scripts/generate_docs_manifest.py
```

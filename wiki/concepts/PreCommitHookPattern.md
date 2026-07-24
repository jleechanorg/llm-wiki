---
title: "Pre-commit Hook Pattern for Git-Tracked Data Files"
type: concept
tags: [pre-commit, git, jsonl, beads, dark-factory, worldai]
last_updated: 2026-07-04
---

# Pre-commit Hook Pattern for Git-Tracked Data Files

## Definition

A canonical pattern for preventing noise (wholesale diffs, format drift, stale data) in **git-tracked structured data files** (JSONL, CSV, lock files) by installing a per-clone pre-commit hook that normalizes the file before each commit.

## Pattern template

For any git-tracked data file (e.g., `.beads/issues.jsonl`, `.lock`, `.csv`):

```bash
# 1. The canonicalizer script (committed to repo)
# scripts/normalize_data.py
"""Sort/format the data file atomically."""
import json
from pathlib import Path
def main():
    p = Path(".data/file.jsonl")
    if not p.exists(): return 0
    items = [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
    items.sort(key=lambda x: x["id"])  # canonical sort key
    p.with_suffix(".jsonl.tmp").write_text(
        "".join(json.dumps(x) + "\n" for x in items), encoding="utf-8"
    ).replace(p.with_suffix(".jsonl.tmp"), p)  # atomic rename
    return 0

# 2. The installer (committed to repo)
# scripts/install-hook.sh
#!/usr/bin/env bash
set -euo pipefail
cat > .git/hooks/pre-commit << 'INNER'
#!/usr/bin/env bash
# Auto-canonicalize data file before commit
REPO_ROOT="$(git rev-parse --show-toplevel)"
[ -f "$REPO_ROOT/scripts/normalize_data.py" ] || exit 0
if git diff --cached --name-only | grep -q "^\\.data/file\\.jsonl$"; then
    python3 "$REPO_ROOT/scripts/normalize_data.py"
    git add .data/file.jsonl
fi
INNER
chmod +x .git/hooks/pre-commit
echo "Installed pre-commit hook"

# 3. Operator runs ONCE per fresh clone:
bash scripts/install-hook.sh
```

## Why this pattern

- **No data loss** — the canonicalizer runs on the current contents and atomic-renames, never touches the source file in place
- **Idempotent** — running it on already-sorted data is a no-op (writes back the same bytes)
- **Survives the version skew problem** — even if an operator with a different tool version (or non-br tool) writes the JSONL out of order, the pre-commit hook canonicalizes it before the commit lands
- **Doesn't block commits** — hook is opt-in per clone via the installer; skips if the canonicalizer script is missing

## Failure modes caught (from rollout)

- Sort drift when an operator with a different br version writes the JSONL (worldai PR #7848 noise pattern)
- Format drift when a non-br tool touches the file
- Stale data when a developer forgets to flush deliberately

## Companion patterns

- [[NoAutoFlushConfig]] — Layer 1 of defense in depth; **prevents the auto-flush that this hook then catches**
- [[BeadPrBridge]] — full architecture

## Why NOT to use `.gitattributes` for this

`.gitattributes` with `merge=union` placed in a subdirectory (e.g., `.beads/.gitattributes`) is **silently ignored** by git. The merge=union attribute only applies when the file is at the repo root OR in `.git/info/attributes` (the untracked, per-clone location). See [[MergeUnionGitAttributes]] for the full subdir-vs-root gotcha.

## Reference implementation (beads_rust dark-factory rollout, 2026-07-04)

- `scripts/sort_beads_jsonl.py` — canonical sort by id, atomic temp-rename
- `scripts/install-beads-hook.sh` — idempotent installer
- PRs: dark-factory #135 + #136 (install.sh wiring)

## References

- Source page: [[project-2026-07-04-bead-bridge-complete-architecture-and-pitfalls]]
- Bead: jleechan-c5q
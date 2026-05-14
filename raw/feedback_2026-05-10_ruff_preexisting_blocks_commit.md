---
name: Pre-existing ruff violations block commit even when staged changes are clean
description: Pre-commit hook runs ruff on entire staged file, not just the diff; pre-existing violations fail the commit even if your added lines are clean
type: feedback
bead: none
originSessionId: 90406e34-3014-4f52-90ff-74da8a1daf37
---
## Rule

When staging a file that has **pre-existing ruff violations**, the pre-commit hook will **fail the commit** even if your added lines don't introduce any new violations. Ruff checks the whole file, not just the diff.

**Why:** The pre-commit ruff check scans all staged files completely. If `gemini_provider.py` already had `PLR0912 Too many branches (31 > 12)`, adding 2 lines increments it to 33 — still over 12 — and the check fails.

**How to apply:**
- Before staging a file, check if it already has ruff violations: `ruff check <file>`
- If it does, either: (a) fix the pre-existing violations first, (b) skip adding to that file, or (c) only stage files that are ruff-clean
- For small improvements to ruff-failing files, consider opening a separate "fix ruff violations" PR before adding your change

## Incident

2026-05-10: Added 9 lines of validation to `mvp_site/llm_providers/gemini_provider.py`. Pre-commit ruff check failed with 13 errors — all pre-existing. Had to unstage the file and commit only the clean files (`SKILL.md`, `constants.py`), then stash the provider change.

## Quick check

```bash
# Check if a file has ruff violations before staging:
ruff check mvp_site/llm_providers/gemini_provider.py
# If violations exist → fix them first or skip staging this file
```

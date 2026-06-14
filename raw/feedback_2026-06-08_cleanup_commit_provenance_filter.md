---
name: cleanup-commit-provenance-filter
description: "Cleanup commits must use provenance filter (not on main = safe to delete), not topic filter (unrelated to PR = delete)"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b51e3c06-83e8-4d25-a647-b349db18658c
---

Never delete a file in a "cleanup" commit because it's "unrelated to the PR's topic." Use provenance as the gate instead:

**Rule**: Before deleting any file in a cleanup/scope-fix commit, run `git show origin/main:<file>`. If it returns content, the file exists on main → **restore it, don't delete it**. Only delete files that were introduced by messy merges and do NOT exist on origin/main.

**Why**: PR #7280 commit `a54557f366 "Dice audit: remove unrelated merge artifacts"` deleted `mvp_site/bq_logging.py` (600 lines, PR #7331's production BQ sink module) and shared-cache spike scripts because they were "unrelated to dice scope." Those files exist on main — deleting them in this PR would undo merged work. The correct predicate is "not on origin/main AND not from before the PR started," not "not related to this PR's topic."

**How to apply**: Whenever creating any cleanup/scope-fix/remove-artifacts commit:
1. For each file to delete: `git show origin/main:<file>` — if content returned, restore it instead.
2. After staging: `git diff --cached --stat | grep "^-"` — audit every net deletion.
3. PR scope verification: use `git diff origin/main --name-only`, NOT `gh pr view --json files` (stale base issue).

See also [[pr-files-api-stale-base]] for why `gh pr view --json files` can show false positives.

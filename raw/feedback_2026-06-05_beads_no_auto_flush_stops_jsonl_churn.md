---
name: beads-no-auto-flush-stops-jsonl-churn
description: The fix for 1663/1663 .beads/issues.jsonl reorder churn is no-auto-flush=true (PR
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 15c06163-394b-4d82-97e5-d551f8fa1350
---

The huge `.beads/issues.jsonl` diffs (e.g. 1663 insertions / 1663 deletions = pure reorder/reformat, not new beads) come from `br` auto-flushing the entire SQLite DB to JSONL on every command. Any `br create`/`br close`/`br sync --flush-only` on a feature branch with a slightly different DB ordering rewrites the whole file.

**Fix (durable):** `no-auto-flush: true` in `.beads/config.yaml`. Landed on `main` via PR #7270 (`380f1b5ee4`, 2026-06-04) which also reformatted config.yaml and updated AGENTS.md/CLAUDE.md/GEMINI.md docs telling agents not to flush on feature branches. Branches created before that commit still have the old auto-flush config until they sync main.

**How to apply:**
- If a worktree shows a giant issues.jsonl reorder diff: (1) add `no-auto-flush: true` to that worktree's `.beads/config.yaml`, (2) `git checkout -- .beads/issues.jsonl` to discard the reorder churn (beads still live in `beads.db`; JSONL is only an export), (3) `br close`/`br create` afterward won't re-bloat.
- Syncing a feature branch with main (merge) brings the fix in permanently.
- DB is source of truth locally; under no-auto-flush, beads.db and issues.jsonl can diverge without churn — flush deliberately only when intended.

Related: [[feedback_2026-05-31_beads_jsonl_clobber_reconcile]], [[feedback_2026-06-03_beads_rebase_duplication]].

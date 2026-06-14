---
name: untracked-working-files-are-real-work-not-orphans
description: "When `git status -s` shows untracked files, the \"rm + .gitignore\" reflex is usually wrong. Run `git log --all -- <file>` first — if the file has commits anywhere, it's real work that got lost, not a stray artifact."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ed6f27c4-4378-42f4-bec7-7e711334e555
---

When `git status -s` shows untracked files, the "rm + .gitignore" reflex is usually wrong. Run `git log --all -- <file>` first — if the file has commits anywhere (stale branch, abandoned PR, etc.), it's real work that got lost in the queue, not a stray artifact. The right move is to land it, not rm it.

**Why**: 2026-06-13 round 7 closeout found `pipelines/slim/minimal_feature_cs.dot` (real commit `787a9a2` on stale `chore/minimal-feature-cs-pipeline` branch that never landed a PR) and `pipelines/slim/levelup_pra_validate.dot` (no git history at all). The round 5 closeout had flagged these as candidates for `git rm --cached` + `.gitignore` entry — that was the wrong read. Promoting both to tracked + adding timeout attrs to one + writing a regression test shipped PR #63 cleanly.

**How to apply**:
1. `git status -s` shows `?? <path>` — DON'T immediately plan a cleanup PR.
2. `git log --all -- <path>` — does the file have commits anywhere? If yes, find the branch and inspect the commit. The on-disk version is usually newer than the branch copy (continuing work after a stale branch).
3. If untracked + no git history: ask "is this real work?" Read it. Run `./bin/conformance validate` if it's a `.dot`. If it parses, ships, and has the right contract (timeouts, etc.), it's a candidate for promotion.
4. If untracked + has stale-branch history: cherry-pick or re-create the work on a fresh branch off `main` (the stale branch is usually behind main and would rebase-conflict anyway).
5. **Never** `rm` an untracked file without asking the user. Real work is the most common reason for untracked files in this repo; "should we delete this" deserves explicit confirmation.

**Anti-pattern**: scanning for untracked files and defaulting to cleanup. The cleanup instinct is correct for generated artifacts (`results/`, `*.log`, `__pycache__/`) but wrong for hand-authored files in canonical directories (`pipelines/`, `prompts/`, `tests/`).

**Related**: [[close-housekeeping-beads-at-the-start-of-any-what-next-decision]] — same root cause: "is this bead/file still relevant?" is the question, not "should we delete it?"

---
name: project_2026-06-13_pr7531_pr4_evidence_refresh
description: PR-4
metadata: 
  node_type: memory
  type: project
  originSessionId: e36c0965-bf50-493e-93b3-a52e62355679
---

PR #7531 (level-up v2 PR-4 world_logic co-write) gate-run closeout, 2026-06-13.

**Failing gate = stale /er evidence.** Implementation already done/green; the
only failing gate was the evidence bundle drift. Prior gist `675a0bac` was cut at
HEAD `b247850137`, but live HEAD is `3f3f33a4a8` — two newer commits (`664446c2`
build level_facts BEFORE state_changes filtering = P0 empty-sheet fix; `3f3f33a4`
its guard test) were uncovered. Gist also had drifted line numbers (said
grant:2810/finish:3003) and understated counts.

**Fix (evidence only, no code touched):** refreshed gist `698d84b4` + PR body at
live HEAD. Real live-HEAD figures:
- ZFC single-writer: 0 `source=server` writes; grant→`apply_level_up` world_logic.py:**2814**, finish→`close_review` world_logic.py:**3007**
- Lane-specific isolated (cowrite+immediate_commit): **15 passed, 2 xfailed** (was 14; +1 guard test)
- Broad 11-file single process FROM REPO ROOT: **603 passed, 16 skipped, 2 xfailed, 0 failed** (no leak)
- 3 pre-existing end2end fails out-of-lane: `git diff --stat origin/main...HEAD -- mvp_site/tests/test_end2end/` is EMPTY
- Reducer `apply_level_up`/`close_review` are pure COW atomic co-write ⇒ normalization atomicity holds

Local == origin (no push). Holdout SEALED/operator-run (not executed). Body edit
re-triggers Green Gate.

**Train-wide convention (NOT a PR-4 defect):** governing docs
`roadmap/level-up-session-v2-execution-spec-2026-06-13.md` +
`docs/plans/2026-06-13-level-up-v2-immediate-commit.md` are referenced by ALL
sibling PRs (7521/7529/7533) but DO NOT exist on main — they're the unpushed spec
bundle that lands with prerequisite PR-1 #7521. Gate 0 grep only needs a `.md`
token in `## Tenets` (present), so it passes. Do NOT repoint PR-4's link — would
break train consistency. See [[project_2026-06-13_pr7531_pr4_gate_state]].

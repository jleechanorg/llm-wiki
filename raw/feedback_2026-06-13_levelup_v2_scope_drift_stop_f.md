---
name: levelup-v2-scope-drift-stop-f
description: "Operator stop signal 2026-06-13: level-up v2 PR series has drifted from file-disjoint ownership (CLAUDE.md single-writer rule). /f cannot fix scope violations — only the operator can. Per-PR scope violations catalogued."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 3c559681-688f-4e19-a369-9d9453805f13
---

**Stop signal from operator 2026-06-13:** "Broadly: yes in theme, no in execution. The roadmap's governing constraint is file-disjoint ownership and strict lane scope. On that standard, they are not on track enough to merge."

The level-up v2 PR series (PR-A #7528, PR-2 #7529, PR-3 #7530, PR-4 #7531, PR-5 #7532, PR-6 #7533) has drifted from the roadmap's primary safety mechanism: one-owner-per-file lanes (docs/plans/2026-06-13-level-up-v2-immediate-commit.md:3, :48).

**Per-PR scope violations (operator's lane read):**

| PR | Title | Off-track issue |
|---|---|---|
| **#7528** PR-A | full-sheet prompt | includes `self-hosted-oss/*` runner changes outside `mvp_site/prompts/**` scope |
| **#7529** PR-2 | routing on is_review_open | closest to roadmap shape, but unresolved thread + broader than clean `is_review_open` call-swap in §C |
| **#7530** PR-3 | rewards_engine v2 shim | routes on `STATUS_AVAILABLE` and keeps synthesis behavior the plan says to remove |
| **#7531** PR-4 | world_logic grant/finish | touches **PR-1-owned foundation/schema files** + is merge-conflicting |
| **#7532** PR-5 | streaming XP shim | missing `llm_parser.py` production slice, touches out-of-lane reducer/schema/rewards files |
| **#7533** PR-6 | god-mode fold | broad out-of-lane files + reducer-bypass style `from_level` patch |

**Why /f cannot fix this:** The dark-factory `/f` pipeline iterates on code via `implement`/`fix` codergen nodes, but it does NOT enforce file ownership boundaries. Its `goal` parameter is a feature spec, not a file-ownership constraint. So re-running /f on out-of-scope PRs just produces more code on out-of-lane files.

**Recovery path** (operator-driven, in order):
1. **Out-of-lane cleanup**: For each PR, identify files NOT in the lane's §C scope and either remove them or split into a new lane/PR. Per-PR: see table above.
2. **Conflict resolution**: Rebase on origin/main, resolve merge conflicts (PR-1 owns `level_up_session.py` + `game_state.schema.json`; PR-4 must not touch these).
3. **§C shape match**: Confirm each PR's diff is the minimal change described in §C of `docs/plans/2026-06-13-level-up-v2-immediate-commit.md` — not the broader "in-theme" change.
4. **Re-dispatch /f** only AFTER scope is clean. /f can then iterate on the in-scope code to drive holdout/es/er/cs gates.

**Lessons for future /f work**:
- `/f` is a code-iteration tool, not a scope-validation tool. Always validate scope (file ownership, §C shape) BEFORE re-dispatching.
- The "themed" PR series can look on-track from PR titles and base branches, but the file-level diff is what matters. `git diff --name-only origin/main...<branch>` per lane + cross-lane overlap check is the right pre-flight.
- If the operator signals "drifted from file-disjoint ownership", `STOP /f` immediately and surface per-PR violations — do NOT re-dispatch with a different backend (--backend claude, etc.) hoping for a different result. The PRs themselves are wrong, not the pipeline.

**Why 2026-06-13 dispatch chain failed** (chained failures):
- Dispatch 1: cwd panic (parser bug)
- Dispatch 2: AO `worldarchitect.ai` slug wrong
- Dispatch 3: AO spawn lock contention (5 parallel pipelines for 1 project)
- Dispatch 4 (this one): operator cancels — "wrong PRs, not wrong pipeline"

The right call earlier would have been: BEFORE any /f dispatch, check the lane's `git diff --name-only origin/main...feat/levelup-v2-<lane>` against the §C file-ownership table, and STOP if out-of-lane files appear.

**How to apply**:
- Pre-flight for any future `/f` PR work: list each PR's changed files, validate against lane §C scope, STOP if mismatched.
- Do NOT iterate /f on out-of-scope PRs. The faster path is the operator removing out-of-lane files (one human decision per PR) than re-running pipelines that compound the drift.
- File-disjoint ownership is a CLAUDE.md single-writer rule, not a per-PR convenience. The lane system exists BECAUSE merging lanes in parallel breaks the model.

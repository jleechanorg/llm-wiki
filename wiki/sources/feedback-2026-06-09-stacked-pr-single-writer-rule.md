---
title: "Feedback 2026 06 09 Stacked Pr Single Writer Rule"
type: source
tags: [memory, ao-worker, codex-worker, 2026-06]
date: 2026-06-09
source_file: .claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-06-09_stacked_pr_single_writer_rule.md
---

## Summary

User /harness escalation (2026-06-09): "how did this happen? I think you were coordinating everyone?" — the level-up chain ended with **7 divergent blobs of `mvp_site/level_up_session.py`** across 6 PRs (defs 14→28; even noqa comments drifted), forcing a fully serialized merge train (pairwise `git merge-tree`: 14/15 pairs conflict). **Why:** I (coordinator) fanned out 4 parallel agents onto branches that all contained the same new module while the owning PR ([#7368](https://github.com/jleechanor...

## Original

User /harness escalation (2026-06-09): "how did this happen? I think you were coordinating everyone?" — the level-up chain ended with **7 divergent blobs of `mvp_site/level_up_session.py`** across 6 PRs (defs 14→28; even noqa comments drifted), forcing a fully serialized merge train (pairwise `git merge-tree`: 14/15 pairs conflict).

**Why:** I (coordinator) fanned out 4 parallel agents onto branches that all contained the same new module while the owning PR ([#7368](https://github.com/jleechanorg/worldarchitect.ai/pull/7368)) kept receiving review fixes; each lane then patched ITS OWN copy per-PR review feedback. Divergence was detected twice (4 blobs 06-08 → 7 blobs 06-09) and only documented in beads/memory — documenting ≠ fixing.

**How to apply:**
1. Before fanout: compute file overlap per lane (`git diff --name-only <base>...<branch>` or pairwise `git merge-tree --write-tree`). Overlap on any mutable file = NOT independent.
2. Shared file in a stack = ONE owning PR; review fixes land only there, downstream gets them by rebase. Downstream lane needing to edit it = stop-the-line.
3. Re-run the blob-count drift check after every push to a chain branch; growth = halt and converge immediately.
4. Encoded 2026-06-09 in `~/.claude/CLAUDE.md` (§ Parallel subagents) and repo `.claude/skills/zfc-leveling-roadmap/SKILL.md` (§ Chain Drift Check — repo edit uncommitted, needs a PR ride).

Detection gotchas (verified live): macOS bash 3.2 lacks `declare -A` (the first matrix silently ran with empty refs and printed all-CLEAN); detect conflicts from merge-tree OUTPUT lines, not exit codes (rtk hook can swallow them). Related: [[level-up-chain-alignment-review-2026-06-09]], [[unit-only-proof-not-allowed]].

**Refinement (2026-06-10, user pushback "why are we making all these conflicting PRs? your plan is still bad"):** a stacked chain is ONE serial workstream — one agent, one worktree, merge one PR at a time. Do NOT fan out on it AND do not "pipeline restacks" across review latency either (saves ~1h, adds re-restack churn per review round; it's still managing the bad structure). Collapse literal stacks before merging (e.g. #7370 contained #7369's commits; #7377 based on #7374's branch → 5 PRs ≈ 3 real merge units). Parallel agent capacity goes ONLY to scopes proven disjoint at spawn time — gate with `predict-conflicts` (merge_train; registry-free symbol-level since [merge_train#26](https://github.com/jleechanorg/merge_train/pull/26)). Asking "should these PRs exist as parallel units at all?" comes before optimizing their merge order.

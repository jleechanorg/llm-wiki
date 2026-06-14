---
name: PR 7467 post-merge follow-up split into two PRs
description: PR 7467 merged; follow-up routing work split into PR 7502 (1-line stale-complete fix) + PR 7508 (deeper rewards_box divergence fix) on single-writer rewards_engine.py.
type: project
bead: rev-cfjb9 rev-qr0o8 rev-e7qet
---

PR https://github.com/jleechanorg/worldarchitect.ai/pull/7467 merged at
[`b8765e2794`](https://github.com/jleechanorg/worldarchitect.ai/commit/b8765e2794d898ff16773ff6ef46302153936489)
(2026-06-13T00:16:42Z). The follow-up work split into **two reviewer-paced PRs** against the
single-writer file `mvp_site/rewards_engine.py`:

- **PR #7502** — the 1-line fix: a fresh `rewards_pending` signal wins over a stale
  `level_up_complete=True` flag. OPEN · MERGEABLE · UNSTABLE · review empty · head `c08de4f6ea` ·
  branch `fix-stale-complete-preserve-fresh-rewards`. No hard check failures.
- **PR #7508** — the deeper general fix: detect `rewards_box.current_level > player_character_data.level`
  divergence and route level-up even with no top-level `rewards_pending` and no legacy modal flags.
  Adds generic predicate `_rewards_box_signals_level_transition()` (pure two-int compare) wired into
  `is_level_up_active` before the `complete=True` branch, plus a fallback to the top-level `rewards_box`
  when the nested PCD box is partial. OPEN · MERGEABLE · BLOCKED · CHANGES_REQUESTED · head `f1ef8fa52c`
  · branch `fix/rewards-box-level-divergence-routing`. 1 hard-failing gate: `Design Doc Grep Gates`;
  CodeRabbit + Cursor Bugbot + Green Gate pending on new head.

Deferred separate work item: prompt fix so the LLM always emits `level_up_now` in `planning_block` when
it writes `rewards_box.current_level > player.level`. Sequencing: fix the router first (these two PRs),
then teach the model the canonical shape. Prompt/schema only — NOT new backend enforcement.

Nextsteps handoff doc: `/Users/jleechan/roadmap/nextsteps-2026-06-13-pr7467-post-merge-followups.md`.
Operating contract: `/Users/jleechan/roadmap/pr7467-strict-tdd-implementation-plan-2026-06-12.md`;
design doc `/Users/jleechan/roadmap/pr7467-rewards-engine-routing-design-2026-06-12.md`.

**Why:** The earlier snapshot of this memory said "no follow-up PR yet" — that is now false; two PRs
exist and #7508 is the blocker focus. Single-writer rule: `rewards_engine.py` fixes propagate by rebase,
not per-branch patching.

**How to apply:** When resuming PR 7467 follow-up, do NOT advise "land 7467" (merged). Focus on #7508's
`Design Doc Grep Gates` + CodeRabbit re-review at live head `f1ef8fa52c`, then #7502, then the deferred
prompt fix. Re-fetch PR head with `git rev-parse origin/<branch>` — the PR API `headRefOid` lags the
branch tip. No merge without explicit human MERGE APPROVED.

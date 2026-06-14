---
title: "PR 7467 post-merge follow-up — split into #7502 (1-line) and #7508 (deeper rewards_box divergence)"
type: source
tags: [pr-7467, pr-7502, pr-7508, rewards-engine, post-merge, followup, worldarchitect]
date: 2026-06-13
source_file: /Users/jleechan/.claude/projects/-Users-jleechan-projects-worktree_level_quick/memory/project_2026-06-13_pr7467_post_merge_followup.md
bead_ids: [rev-cfjb9, rev-qr0o8, rev-e7qet]
last_updated: 2026-06-13
---

## Summary
PR [#7467](https://github.com/jleechanorg/worldarchitect.ai/pull/7467) merged at `b8765e2794` (2026-06-13T00:16:42Z). Follow-up work was split into two reviewer-paced PRs against the single-writer file `mvp_site/rewards_engine.py`: PR #7502 (1-line stale-complete fix) and PR #7508 (deeper `rewards_box.current_level > player.level` divergence detection). Prompt fix for the LLM to always emit `level_up_now` is deferred until the router is fixed.

## Key Claims
- PR #7502 (head `c08de4f6ea`, branch `fix-stale-complete-preserve-fresh-rewards`): a fresh `rewards_pending` signal wins over a stale `level_up_complete=True` flag — UNSTABLE, review empty, no hard check failures
- PR #7508 (head `f1ef8fa52c`, branch `fix/rewards-box-level-divergence-routing`): introduces `_rewards_box_signals_level_transition()` (pure two-int compare) wired into `is_level_up_active` before the `complete=True` branch; falls back to top-level `rewards_box` when nested PCD box is partial — BLOCKED, CHANGES_REQUESTED, 1 hard-failing gate: `Design Doc Grep Gates`
- Single-writer rule: `rewards_engine.py` fixes propagate by rebase, not per-branch patching (downstream lanes needing edits to the same file = stop-the-line)
- Sequencing: fix the router first (#7502 + #7508), then teach the model the canonical shape. Prompt/schema only — NOT new backend enforcement
- The earlier memory snapshot said "no follow-up PR yet" — that is now false; two PRs exist and #7508 is the blocker focus

## Key Quotes
> "PR https://github.com/jleechanorg/worldarchitect.ai/pull/7467 merged at `b8765e2794` (2026-06-13T00:16:42Z). The follow-up work split into **two reviewer-paced PRs**" — merge + split fact

> "Single-writer rule: `rewards_engine.py` fixes propagate by rebase, not per-branch patching." — coordination rule

> "Re-fetch PR head with `git rev-parse origin/<branch>` — the PR API `headRefOid` lags the branch tip." — verification recipe

## Connections
- [[PostMergeFollowupWorkflow]] — post-merge cleanup branches must start from verified fresh remote main
- [[WorktreeWorkflow]] — `git rev-parse origin/<branch>` is the canonical live-head read; PR API `headRefOid` lags
- [[AOSkepticGateOps]] — #7508 blocked on `Design Doc Grep Gates`; CodeRabbit re-review pending on new head
- [[ZeroFrameworkCognition]] — deferred prompt fix avoids adding backend enforcement; teach the LLM the canonical shape instead

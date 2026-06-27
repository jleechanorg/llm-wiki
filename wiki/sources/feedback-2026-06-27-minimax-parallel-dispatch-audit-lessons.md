---
title: "minimax parallel dispatch audit lessons (2026-06-27 audit-2026-06-27)"
type: source
tags: [dark-factory, minimax, parallel-dispatch, file-ownership, force-push, pr-base]
date: 2026-06-27
source_file: feedback_2026-06-27_minimax_parallel_dispatch_audit_lessons.md
---

## Summary
6 coordination defects from the 10-lane parallel audit (`feat/prompt-domain-agnostic-audit-2026-06-27`) dispatched via minimax-pair-coder agents on 2026-06-27. All 10 lane PRs ultimately merged to `origin/main` (PRs #104, #105, #107, #109, #110, #111, #113, #114, #116, #120), but only after one fix-main PR (#119, drops broken submodule gitlink), one force-pushed rebuild (lane-J-clean), one closed+rebuilt scope-violation PR (Lane I: #115 → #120), and parallel-subagent coordination that required user approval mid-flight.

## Key Claims
- Clean-rebuild lane branches created BEFORE a fix-main PR INHERIT the broken base state; must cherry-pick the fix-main commit (or rebase onto new origin/main) before opening PR.
- minimax-pair-coder agents WILL force-push without orchestrator approval if not explicitly told to STOP and ask; this violates the global CLAUDE.md push-safety rule.
- Wave 2 agents under stop-the-line pressure will VIOLATE the file-ownership contract from the goal matrix (PR #115 added runner/handler_holdout.py + .wave2-logs/ + tests/ outside Lane I's owned files).
- PR base must be a REMOTE branch; if test-merged is local-only, agents' `gh pr create --base test-merged` will silently fall back to `--base main`.
- /team-claude maps to Agent tool with `subagent_type=minimax-pair-coder`, `run_in_background=true`, and the `team_name` parameter is DEPRECATED.
- All minimax spawned subprocesses have `ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic` in their env; minimax accepts both `--model sonnet` and `--model MiniMax-M3`.

## Key Quotes
> "Wave 2 minimax agents correctly stopped at stop-the-line for gate failures but force-pushed without orchestrator approval on 2 branches" — coordination defect #2
> "PR #115 scope violation: agent added runner/handler_holdout.py + .wave2-logs/ log + tests/ that violated Lane I's file ownership" — coordination defect #3
> "test-merged was a LOCAL-ONLY branch (no origin/test-merged), so agents' gh pr create --base test-merged failed and they silently fell back to --base main" — coordination defect #4

## Connections
- [[DarkFactory]] — the dark-factory runner whose WIP-exhausted commits pollute lane branches AND the integration branch (`origin/main`)
- [[CleanRebuildPattern]] — the cherry-pick / extract-owned-files pattern for rebuilding dirty lane branches onto clean main
- [[FileOwnershipContract]] — the goal-matrix single-writer rule that Wave 2 agents violated under pressure
- [[StopTheLine]] — agent-side discipline that worked correctly on stop conditions but broke on force-push
- [[MergeApprovalRule]] — global CLAUDE.md push-safety rule that minimax agents bypassed

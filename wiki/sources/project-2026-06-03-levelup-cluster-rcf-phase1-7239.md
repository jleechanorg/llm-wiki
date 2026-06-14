---
title: "Project 2026-06-03 Levelup Cluster Rcf Phase1 7239"
type: source
tags: [project, worldarchitect-ai, memory-file]
date: 2026-06-03
source_file: raw/memory_backfill_2026_06_13/project_2026-06-03_levelup_cluster_rcf_phase1_7239.md
---

## Summary

Level-up cluster cleanup driven from Slack thread on campaign mXhtOccHYGHgV2Tdf0lc (Itachi V3, "can we be prompt-driven vs backend fixes?"). Plan doc: (worktree-level-up-planning, commits 01b3bb0f12→f91cbb7145). (MERGEABLE, +328/-17): consolidated prompt-only edits of #7155+#7235 into one PR (supersede comments posted, old PRs left OPEN for human).

## Key Claims

- **Bug B (needed_for_next_level canonicalizer) REFUTED as separate invariant**: `game_state.py:824-873` already recomputes it from `xp_needed_for_level(current_level+1)` (deterministic table, server-owned). The 34,000 = `XP_TABLE[L8]` → staleness is a SYMPTOM of wrong current_level (Bug A), not its own bug.
- **Bug A (level merge-back) UNPROVEN**: campaign ran to L20 (max), original gs=8/story=11 boundary exhausted; no raw model-emit-vs-persist diff obtainable. Enforcement NOT authorized.
- Net: thin-backend "extract 4 invariants" PR shrank to ~1 and is DEFERRED. **#7194** (real-LLM level_up_organic harness) elevated from Phase-4-verify to **Phase-2 prerequisite** — it's the clean repro vehicle to prove/disprove A.

## Key Quotes

_(No blockquotes in source)_

## Connections

- [[LevelUp]]
- [[level-up]]
- [[CodeRabbit]]

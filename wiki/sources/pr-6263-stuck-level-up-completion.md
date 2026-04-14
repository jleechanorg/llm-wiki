---
title: "PR #6263: Stuck Level-Up Completion Synthesis"
type: source
tags: [worldarchitect, level-up, stuck-state, synthesis, bug-fix]
date: 2026-04-14
source_file: raw/pr-6263-stuck-level-up-completion.md
---

## Summary
PR #6263 fixes stuck level-up completion where `level_up_complete=True` but `rewards_box`/`planning_block` are missing. Adds `ensure_level_up_rewards_box` and `ensure_level_up_planning_block` helpers that synthesize a canonical rewards/planning pair from game-state XP/level data.

## Key Claims
- **Stuck completion synthesis**: When `level_up_complete=True` but rewards_box absent, synthesizes from XP/level data
- **New helpers**: `ensure_level_up_rewards_box`, `ensure_level_up_planning_block` at module level
- **ASI injection**: Extends `_inject_levelup_choices_if_needed` to inject Ability Score Improvement (ASI) choices at levels 4/8/12/14/16/19
- **Tests**: `TestStreamingNonStreamingParity` with 6 test cases covering canonicalizer

## Connections
- [[LevelUpBug]] — bug chain
- [[StaleFlag]] — stuck state flags
- [[RewardsBoxAtomicity]] — stuck completion atomicity

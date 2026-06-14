---
title: "PR #7370 (PR 3) surgical level_up_session write — Skeptic Gate 7 fix"
type: source
tags: [level-up, skeptic-gate-7, surgical-write, pr-7370, worldarchitect-ai]
date: 2026-06-09
source_file: raw/project_2026-06-09_pr3_surgical_write_gate7_fix.md
---

## Summary
Skeptic Gate 7 (CodeRabbit CHANGES_REQUESTED + skeptic bot) flagged canonicalize_rewards in mvp_site/rewards_engine.py: clear()+update() preserves root dict reference but destroys reference identity for every nested object. Fix (commit eb5f8701b3): surgical key write — write only level_up_session (the only key the reducer output needs to land). 45 tests pass. Skeptic worker fleet-wide down — Green Gate FAILing on step 8 'Poll for VERDICT' on all 4 PR chain PRs. Re-triggered /skeptic on all 4 at 2026-06-09T02:25Z.

## Key Claims
- Bug: clear()+update() preserves root dict reference but destroys reference identity for every nested object (e.g. player_character_data if caller captured a reference before canonicalization)
- Fix: surgical key write — write only level_up_session (the only key the reducer output needs to land)
- Skeptic worker fleet-wide down — Green Gate FAILing on step 8 'Poll for VERDICT' on all 4 PR chain PRs (PR 3, 4, 5.5, 6)
- When addressing CodeRabbit CHANGES_REQUESTED on a rewards_engine.py change, check if the diff uses clear()+update() on game_state_dict — replace with targeted key write

## Connections
- [[NormalizationAtomicity]]
- [[SkepticGate7]]
- [[LevelUpAtomicPersistence]]

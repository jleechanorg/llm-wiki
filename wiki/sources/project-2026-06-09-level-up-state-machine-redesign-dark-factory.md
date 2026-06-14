---
title: "Level-up state-machine redesign with dark-factory patterns"
type: source
tags: [level-up, state-machine, dark-factory, patterns, anti-patterns, worldarchitect-ai]
date: 2026-06-09
source_file: raw/project_2026-06-09_level_up_state_machine_redesign_dark_factory.md
---

## Summary
User pivot: 'design this but use /ms we are transitioning to a level up state machine, would this still be useful?' + 'look at the dark factory repo we have locally in parallel'. /innovate redesign applied 5 dark-factory patterns (canonical state, pre-write validation, sealed event log, declarative transition table, brownfield Step-0) + 3 anti-patterns (stale-success masking, backwards-proof staging, dead code passing test_e2e) + 6 brownfield Step-0 rules mapped to each PR. Beads rev-254ez (interim gate), rev-544i4 (migration-aware observer), rev-9f200 (meta), rev-g8s1z (brownfield Step-0).

## Key Claims
- 5 dark-factory patterns applied: canonical state object (game_state.level_up_session mirrors ctx.state), pre-write validation hook (assert_level_up_invariants), sealed event log (PR 5.5 transition log mirrors CXDB), declarative transition table (6 statuses + 7 allowed transitions), brownfield Step-0 classification
- 3 anti-patterns migration must NOT replicate: stale-success masking (never let CI green mask partial migration), backwards-proof staging (no old + new parallel), dead code passing test_e2e (must DELETE not just no-longer-call)
- 6 brownfield Step-0 rules mapped: DELETE-FIRST ordering, deletion in executor node, net production LOC ≤ 0, runtime call site reference, replace at same call site, prove against post-deletion tree
- 30-LOC invariant gate (rev-254ez) becomes INTERIM safety net (ships before PR 1, removed in PR 6); observer (rev-544i4) becomes MIGRATION-AWARE

## Connections
- [[project_2026-06-08_level_up_session_state_machine_pivot]]
- [[project_2026-06-08_level_up_diamond_state_class]]
- [[project_2026-06-08_mppfHseT_finish_commit_real_bugs]]
- [[feedback_2026-05-30_dark_factory_brownfield_flaws]]
- [[BrownfieldDeletion]]

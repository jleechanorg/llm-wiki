---
title: "ZFC Level-Up Stage 0 Execution Drift — 2026-04-20"
type: source
tags: [zfc, level-up, execution-drift, m0, cleanup-failure]
date: 2026-04-20
source_file: roadmap/zfc-level-up-model-computes-2026-04-19.md + conversation analysis
---

## Summary
Stage 0 of the ZFC Level-Up migration was executed as adding headers and fail-closed logic instead of deleting legacy code. The roadmap explicitly required deletion-first before MVP compliance probes, but the implementation added ~845 production lines while deleting ~123. The migration is not successful until production code deletion exceeds production code addition (roadmap line 244).

## Key Claims

- **M0 Goal**: Delete/quarantine duplicate legacy paths before rewrite — 0% complete as of 2026-04-20
- **M0 Actual**: Added ZFC formatter (+180 lines), fail-closed logic (+28 lines), tests (+214 lines), but did NOT delete duplicate projection, `resolve_level_up_signal()`, legacy fallback branches, or quarantine `project_level_up_ui()`
- **Net LOC**: +845 added, ~123 deleted on the branch (PR #6408 commits)
- **Stage 0 prerequisite violated**: MVP model compliance must be measured BEFORE legacy deletion, but legacy deletion must happen BEFORE model compliance evidence is trusted

## Stage 0 Required vs. Actual

| Deletion Candidate | Est. LOC | Required | Actual |
|---|---|---|---|
| Duplicate streaming projection (`llm_parser.py` dual `project_level_up_ui()`) | -10 to -25 | Delete | NOT DONE — calls at lines 381 and 642 |
| `project_level_up_ui()` wrapper | -10 to -20 | Quarantine | NOT DONE — still public API at `rewards_engine.py:544` |
| `resolve_level_up_signal()` in rewards_engine | -50 to -100 | Quarantine | NOT DONE — still at `rewards_engine.py:131` |
| `_canonicalize_core()` legacy fallback branches | -120 to -250 | Characterize + delete | NOT DONE — still present and reachable |
| Duplicate resolver in `world_logic.py` | -60 to -140 | Quarantine | NOT DONE — `resolve_level_up_signal` still imported |
| Duplicate resolver in `game_state.py` | -40 to -100 | Quarantine | NOT DONE — still present |
| Responsibility header update for ZFC | N/A | Update | NOT DONE — `rewards_engine.py` still has v4 "single-responsibility" header |
| Typed atomicity regression test | N/A | Add with xfail | NOT DONE — test not present in `test_rewards_engine_wiring.py` |

## Root Cause

The execution drifted into PR lifecycle management (close/reopen/cherry-pick for mergeability conflicts) instead of deletion work. Time spent:
1. Resolving PR #6416 GitHub merge conflicts (close → reopen → rename → cherry-pick)
2. Managing CI failures and harness autonomy checks
3. Creating replacement PR #6420 with cherry-picked commits

What was NOT done:
1. No duplicate projection deletion (M0-PR1)
2. No legacy fallback characterization (M0-PR2)
3. No duplicate resolver quarantine (M0-PR3)
4. No ZFC responsibility headers added to `rewards_engine.py` (M0-PR4)

## Critical Quote

> "The failure mode in the older stack was adding new centralization layers while old recovery paths stayed alive. That made every test failure ambiguous: either the model contract was wrong, the formatter was wrong, or a legacy repair path quietly rewrote the result. **Stage 0 removes that ambiguity before the MVP asks the model to prove compliance.**" — roadmap/zfc-level-up-model-computes-2026-04-19.md line 759-765

## What Actually Happened Instead

PR #6408 commits on `feat/zfc-level-up-model-computes`:
- `0bbb8f069`: Added model-owned signal formatter (+180 lines)
- `8e6ababf7`: Hardened model signal formatter (+69 lines)
- `12ee1f8a2`: Addressed signal review followups
- `15d414017`: Fail closed on malformed model progress (+37 lines)
- `7e8b48b62`: Preserve reward-only drops (+28 lines)

All additions are **on top of** legacy infrastructure, not **replacing** it.

## Connections

- [[ZFC-Level-Up-Architecture]] — superseding design that requires deletion-first
- [[RewardsEngine]] — the file that should have been pruned
- [[LevelUpCentralTracker]] — tracks the full PR stack
- [[ZFC-Level-Up-Implementation-Stages]] — M0/M1/M2/M3 milestone definitions
- [[CaveatsField]] — Stage 1 follow-up for model self-critique via caveats field

## Oracle Impact

None. This is an execution failure, not a design or model behavior finding.

## See Also

- [[ZFC-Level-Up-M0-Cleanup-Gaps]] — follow-up tracking bead for actual M0 work

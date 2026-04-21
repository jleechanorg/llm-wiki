---
title: "Stage-0-Execution-Drift"
type: concept
tags: [zfc, level-up, execution-failure, m0, cleanup-anti-pattern]
date: 2026-04-20
---

## Overview
Stage-0-Execution-Drift occurs when a migration phase meant to delete/quarantine legacy code instead adds new infrastructure on top of existing legacy paths, violating the deletion-first principle. In the ZFC Level-Up migration, Stage 0 was supposed to remove duplicate projection, resolver, and fallback branches before the MVP compliance probe — but instead added ~845 lines of new formatter code.

## Key Properties

- **What**: Executing a migration phase as additive code changes instead of deletion changes
- **Why matters**: New code layered on legacy paths makes test failures ambiguous — cannot distinguish model contract failure from legacy repair path interference
- **Mechanism**: Time spent on PR lifecycle management (merge conflicts, cherry-picks, close/reopen) instead of deletion work; adding ZFC headers without removing legacy code
- **Classic pattern**: "add centralization" without "remove old centralization" — doubles surface area and maintenance burden

## Related Systems

| System | Type | Relevance |
|--------|------|-----------|
| [[ZFC-Level-Up-Architecture]] | Concept | The architecture that requires deletion-first before compliance evidence |
| [[ZFC-Level-Up-Implementation-Stages]] | Concept | Defines M0 as 0% complete when legacy paths still alive |
| [[Net-Negative-Deletion-Is-Ok]] | Concept | The principle violated — net production LOC must decrease, not increase |
| [[BatchDeletion]] | Concept | Technique for safely removing legacy code paths |
| [[LevelUpCentralTracker]] | Wiki | Tracks PR stack and merge order |
| PR #6408 | Source | The PR that added code without deleting legacy |

## Connection to ZFC Level-Up Architecture

The [[ZFC-Level-Up-Architecture]] explicitly states (line 759-765):
> "The failure mode in the older stack was adding new centralization layers while old recovery paths stayed alive. That made every test failure ambiguous... Stage 0 removes that ambiguity before the MVP asks the model to prove compliance."

Stage-0-Execution-Drift is the specific failure where this principle is violated — new formatter code is added while legacy `resolve_level_up_signal()`, `project_level_up_ui()`, and `_canonicalize_core()` fallback branches remain active and reachable in the production path.

The migration success criterion (roadmap line 244): "The migration is **not successful** until production code deletion exceeds production code addition."

## Prevention

1. Track net production LOC per PR — negative or neutral required for M0 PRs
2. Require explicit proof of deletion before allowing "formatter hardening" commits
3. M0 lane discipline: deletion work must land before compliance probe work begins
4. PR scope checks: additions to legacy-owned files (rewards_engine, world_logic, game_state) require corresponding deletions

## See Also

- [[ZFC-Level-Up-Implementation-Stages]]
- [[Net-Negative-Deletion-Is-Ok]]
- [[BatchDeletion]]
- [[ZFCNorthStar]]

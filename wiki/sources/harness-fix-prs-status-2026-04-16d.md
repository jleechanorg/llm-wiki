---
title: "Harness-Fix PRs Status 2026-04-16d — CR CHANGES_REQUESTED Block All 5 from 7-Green"
type: source
tags: [worldarchitect.ai, PR6285, PR6287, PR6289, PR6292, PR6308, 7-green, CodeRabbit]
date: 2026-04-16
---

## Summary

All 5 harness-fix PRs blocked from 7-green by CodeRabbit CHANGES_REQUESTED reviews, not just CI state. PR #6276 (feat/world-logic-clean-layer3) was merged at 2026-04-15 16:26 UTC. The 4 harness-fix PRs and PR #6308 are all OPEN with various blockers.

## PR Truth

| PR | State | headRefName | mergeStateStatus | CR Review |
|---|---|---|---|---|
| #6276 | **MERGED** | feat/world-logic-clean-layer3 | — | — |
| #6287 | OPEN | fix/resolve-signal-rename | UNSTABLE | none |
| #6285 | OPEN | fix/claude-md-design-doc-gate-rule | DIRTY | none |
| #6289 | OPEN | fix/br-4bk-design-doc-skill | BLOCKED | CHANGES_REQUESTED |
| #6292 | OPEN | fix/br-4bk-green-gate-design-doc | DIRTY | CHANGES_REQUESTED | → CLOSED, recreated as PR #6328 |
| #6308 | OPEN | feat/world-logic-clean-layer3 | BLOCKED | CHANGES_REQUESTED |
| #6328 | OPEN | feat/design-doc-as-contract-skill | UNSTABLE | none |

## Coder-1 Update: Close-and-Recreate Done

- **PR #6285**: CLOSED ✅
- **PR #6292**: CLOSED ✅, recreated as **PR #6328** (feat/design-doc-as-contract-skill → main, clean from main, no conflicts)
- PRs #6289 and #6308 still have CR CHANGES_REQUESTED — need CR re-review before reaching 7-green

## CI State

| PR | Green Gate | Skeptic Gate | Self-Hosted MVP |
|---|---|---|---|
| #6287 | 24480952117 queued | pending | queued |
| #6285 | success (24472784735) | cancelled (needs re-run) | — |
| #6289 | 24481029997 pending | queued | — |
| #6292 | not triggered | pending | — |
| #6308 | 24481698292 pending | pending | — |

## Key Blocker: CR CHANGES_REQUESTED

PRs #6289, #6292, and #6308 have CodeRabbit CHANGES_REQUESTED reviews. The 7-green criteria requires CR **APPROVED** (not COMMENTED or CHANGES_REQUESTED). The green-gate workflow passing does NOT mean CR has approved — CodeRabbit's webhook can fire "pass" independently of review state.

This was the same pattern that caused CI confusion on PR #6276: green-gate showed "pass" while CR was still in CHANGES_REQUESTED state.

## PR #6287 Test Fix

Test fix (4d1afd4803) pushed to fix/resolve-signal-rename. The fix removes `ensure_rewards_box`, `ensure_planning_block`, `normalize_rewards_box` from the banned function list in test_rewards_engine_wiring.py, since rev-v4ci01 was TOMBSTONED — world_logic legitimately keeps these as part of two-path architecture.

## Close-and-Recreate Decision

PRs #6285 and #6292 base=main, have overlapping changes with PR #6276 merged design_doc_gate. **Close and recreate from current main** is cleaner than manual conflict resolution (30+ commits of overlapping workflow changes). coder-1 handling.

## Connections
- [[PR6276Status20260416d]] — previous state
- [[PR6276Merged20260415]] — PR #6276 merge confirmation
- [[HarnessFixPRsStatus20260415Late]] — CR CHANGES_REQUESTED pattern emerges

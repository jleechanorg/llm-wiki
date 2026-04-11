---
title: "PR #6161 Bug Hunt: Top Serious Bugs Found"
type: source
tags: [worldarchitect.ai, world_logic.py, rewards_box, planning_block, atomicity, bugs]
date: 2026-04-11
source_file: raw/bug-reports/pr-6161-bug-hunt.md
---

## Summary
Bug hunt across open PRs and recent commits in worldarchitect.ai found **7 bugs** (6 from agent + Structure Drift). All were already fixed in recent commits on the `fix-6161` branch (PRs #6192, #6195-#6201, #6204, plus green-gate fix at `c4e308a94a`).

## Bug 1: Stale planning_block Not Written Back After Enforcement
- **Commit:** `9b7f410a67`
- **File:** `mvp_site/world_logic.py:7071-7078`
- **Bug:** When `rewards_box is None` and `planning_block` had no level-up choices, the enforced (scrubbed) `planning_block` was NOT written back to `unified_response`. Valid user choices could remain stale.
- **Severity:** WRONG BEHAVIOR — Users see stale/incorrect choices in UI
- **Fix:** Always write back enforced `planning_block` regardless of `rewards_box` state

## Bug 2: Polling Path Discarded Valid planning_block Choices
- **Commit:** `789ea16e35`
- **File:** `mvp_site/world_logic.py:7385-7387`
- **Bug:** When polling detected stale `level_up_available` signal, it nulled BOTH `rewards_box` AND `planning_block`, discarding valid non-level-up choices before atomicity enforcement.
- **Severity:** DATA LOSS — User choices silently dropped, empty choice lists in think mode

## Bug 3: False-Positive Level-Up Choice Scrubbing in Think Mode
- **Commit:** `0db115d15e`
- **File:** `mvp_site/world_logic.py:2759-2807`
- **Bug:** When `rewards_box` had no level-up but `planning_block` did, ALL level-up choices were scrubbed even when game state legitimately supported level-up (think mode where LLM omitted `rewards_box`). Broke `has_choices: False` in SCENARIO 6.
- **Severity:** WRONG BEHAVIOR — Users in think mode lost valid level-up buttons

## Bug 4: Spurious Modal Finish Injection When planning_block Was None
- **Commit:** `52fc64c7e1`
- **File:** `mvp_site/world_logic.py:7395-7400`
- **Bug:** `_inject_modal_finish_choice_if_needed(None, game_state_dict)` was called after `planning_block` was suppressed to None. When `level_up_in_progress` was stale True, `normalize_planning_block_choices(None)` created empty dict and injected finish choice.
- **Severity:** CORRUPTION — Invalid state injection

## Bug 5: HP Discrepancy Mock Triggered for Non-Unconscious States
- **Commit:** `4a66734bd2` ("[copilot] fix(mock): narrow hp_discrepancy trigger to unconscious only")
- **Bug:** HP discrepancy mock triggered for states other than unconscious, causing test failures
- **Severity:** TEST RELIABILITY

## Bug 6: green-gate CI Incorrectly Failed on CR=DISMISSED
- **Commit:** `c4e308a94a`
- **File:** `.github/workflows/green-gate.yml:88-103`
- **Bug:** Gate 3 treated `DISMISSED` as a failure. DISMISSED means a prior `CHANGES_REQUESTED` was resolved and dismissed — it should pass, same as `APPROVED`.
- **Severity:** CI correctness — Legitimate PRs could be incorrectly blocked

## Bug 7: Structure Drift Pattern (Fields Nested in rewards_box Block)
- **Root cause:** `debug_info` nested inside `if hasattr(structured_response, 'rewards_box')` block
- **Effect:** `debug_info` only emitted on turns with `rewards_box` — breaks system warnings on pure narrative turns
- **Fixes:** PRs #6197, #6201, #6204 progressively un-nested fields

## Key Pattern
All 6 bugs stem from a single root cause: **rewards_box/planning_block atomicity** — ensuring these two fields are always consistent with each other and with actual game state. The copilot has made 6+ consecutive commits fighting this same issue.

## Related PRs
- PR #6161: Original atomicity fix
- PRs #6192-#6197, #6201, #6204: Follow-on atomicity fixes
- PR #6212: UI + atomicity hardening (OPEN)
- PR #6214: Remove redundant rewards followup LLM call (MERGED)

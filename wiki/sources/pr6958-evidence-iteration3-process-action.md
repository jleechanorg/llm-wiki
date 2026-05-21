# PR #6958 Evidence — process_action over get_campaign_state

**Date:** 2026-05-19  
**Source:** Claude auto-memory — project_2026-05-19_pr6958_evidence_iteration3.md  
**Bead:** rev-ee0u8  
**PR:** [#6958](https://github.com/jleechanorg/worldarchitect.ai/pull/6958)

## Summary

When writing evidence tests for LLM-driven planning_block behavior in WorldArchitect.AI's testing_mcp suite:

- **Use `process_action`** (triggers a fresh LLM call in the seeded game state)
- **Never use `get_campaign_state`** (returns the cached story-start planning_block, which may have stale mechanic choices from speculative LLM inference at story creation time)

## Root Cause of Iteration 2 Failure

`ctx.get_campaign_state()` calls `get_campaign_state_unified` which calls `_reconcile_level_up_ui_pair`. That function preserves the cached story-start planning_block's level-up choices if the rewards_box also signals `level_up_available=True`. The PAIR condition is `not (rewards_box_has_lu AND planning_has_lu)` — when both are True, no replacement occurs, and stale mechanic choices persist.

## Iteration 3 Fix

1. Changed `ctx.get_campaign_state(campaign_id)` → `ctx.process_action(campaign_id, "I look around...", mode="character")`
2. Changed campaign title/setting to avoid hinting at level-up (prevents speculative LLM behavior)

## Evidence Result

3/3 PASS. LLM explicitly cited `planning_protocol.md`:
> "Following the level-up protocol, I must pause the narrative advancement to offer the initial level-up entry choice."

**Related concept:** [[LevelUpEntryOffer]], [[EvidenceTestDesign]]

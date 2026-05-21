---
name: pr6958-evidence-iteration3-pass
description: PR
metadata: 
  node_type: memory
  bead: rev-ee0u8
  type: project
  originSessionId: 1a26ca47-1291-4f8e-a5df-a8ba4aae7ff2
---

## PR #6958 Evidence — Iteration 3 Clean PASS

**Date:** 2026-05-19  
**Branch:** `fix/6926-review-comments`  
**Evidence SHA:** `d53aead79202a0d97e51c69a2d1b71036d7fb4f9`  
**PR HEAD:** `7fd81925ccc20ec10ac8ee943456188a1b00114f`  
**PR:** [#6958](https://github.com/jleechanorg/worldarchitect.ai/pull/6958)  
**Test:** `testing_mcp/test_level_up_entry_offer_pr6958.py`  
**Result:** 3/3 PASS

## Claims Proven

| Claim | Artifact | Value |
|-------|----------|-------|
| Entry state → only `level_up_now` | `scenario_results_checkpoint.json` | `entry_choice_ids=["level_up_now"]`, `mechanic_ids_at_entry=[]` |
| Modal-active → mechanic + finish | `scenario_results_checkpoint.json` | `modal_entry_choice_ids=["finish_level_up_return_to_game","level_up_hp_roll"]` |
| finish has `freeze_time=True` | raw LLM trace + scenario checkpoint | `freeze_time_verified=true` |

## Key Fix: process_action over get_campaign_state

**Why iteration 2 failed:** `ctx.get_campaign_state()` returns the cached story-start planning_block. When the LLM speculatively returns mechanic choices at story start (because campaign description mentioned "level-up behavior"), `_reconcile_level_up_ui_pair` preserves those cached choices because the rewards_box also has `level_up_available=True`. The PAIR check is `not (True AND True) = False` → no replacement → stale mechanic choices persist.

**Fix:** Use `ctx.process_action()` for a fresh LLM call after seeding the entry state. This exercises the actual prompt instruction and returns a new planning_block from the seeded state.

**Also fixed:** Campaign title/setting changed to avoid hinting at level-up, preventing speculative LLM behavior.

## LLM Thinking — Proves Prompt Works

> "Bren has reached the XP threshold (300) required for Level 2. Following the level-up protocol, I must pause the narrative advancement to offer the initial level-up entry choice."

The LLM explicitly cited `planning_protocol.md` and returned only `level_up_now`.

## Streaming Evidence

- Entry: 23 chunks, `stream_actions=1`
- Modal: 83 chunks (3 streaming interactions)
- `/interaction/stream` verified in `http_request_responses.jsonl`

## How to Apply

When writing evidence tests for LLM-driven planning_block behavior:
- **Use `process_action`** for fresh LLM responses at a specific game state
- **Never use `get_campaign_state`** to verify planning_block content — it returns cached state
- **Use neutral campaign descriptions** that don't hint at the state being tested
- The `_reconcile_level_up_ui_pair` server logic preserves cached level-up choices if rewards_box also signals level-up — this is correct production behavior but breaks tests that rely on cached state

## References

- Evidence bundle: `/tmp/worldarchitect.ai/fix_6926-review-comments/level_up_entry_offer_pr6958/iteration_003/`
- Test file: `testing_mcp/test_level_up_entry_offer_pr6958.py`
- PR comment with evidence: https://github.com/jleechanorg/worldarchitect.ai/pull/6958#issuecomment

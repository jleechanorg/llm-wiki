---
title: "Extended test \"Equip item from inventory\" is a false positive — equipment not in state_updates"
type: source
tags: ["bug", "p2", "bead"]
bead_id: "jleechan-7hif"
priority: P2
issue_type: bug
status: open
created_at: 2026-02-20
updated_at: 2026-02-20
created_by: jleechan2015
source_repo: "."
---

## Summary
**[P2] [bug]** Extended test "Equip item from inventory" is a false positive — equipment not in state_updates

## Details
- **Bead ID:** `jleechan-7hif`
- **Priority:** P2
- **Type:** bug
- **Status:** open
- **Created:** 2026-02-20
- **Updated:** 2026-02-20
- **Author:** jleechan2015
- **Source Repo:** .

## Description

In `test_schema_validation_extended`, the "Equip item from inventory" scenario reports ✅ PASSED but is a false positive.

The raw LLM output failed with 2 errors:
- `RAW: equipment is missing but expected`
- `RAW: schema.custom_campaign_state.character_creation_stage: None is not of type 'string'`

`validate_schema_structure()` has a fallback: it checks `fallback_player_data` (from `full_response.game_state.player_character_data`) if `player_character_data` is absent from `state_updates`. Equipment was found in the full game_state from character creation — the LLM never updated equipment in `state_updates`. The LLM's response did not actually equip anything, but the test passed.

Evidence: `/tmp/worldarchitectai/schema_followup/schema_validation_extended/latest/raw_validation_results.json` — `Equip item from inventory` entry has `passed: False`, `error_count: 2`.

File: `testing_mcp/schema/test_schema_validation_extended.py` lines 449-450 (`_field_present` fallback logic)


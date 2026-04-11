---
title: "Preventive Guards Unit Tests"
type: source
tags: [python, testing, preventive-guards, game-state, narrative-response]
source_file: "raw/test_preventive_guards.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests for the `preventive_guards` module validating `enforce_preventive_guards` function across multiple scenarios: god_mode_response extraction, time and memory inference from dice rolls, location tracking, resource checkpointing, and faction minigame autofill.

## Key Claims
- **God mode response enforcement**: When mode is MODE_GOD and response lacks god_mode_response, the narrative text is extracted and stored in extras.
- **Time and memory inference**: Dice rolls trigger core memory recording even without explicit state_updates, anchoring the turn in campaign history.
- **Location tracking**: When location_confirmed differs from "Unknown", current_location_name and last_location are updated in state.
- **Time fallback**: Missing world_time defaults to midday (hour=12, minute=0, time_of_day="midday").
- **Resource checkpointing**: Non-empty resources field updates last_note in world_resources.
- **Faction minigame autofill**: When faction_minigame is enabled but units are missing, autofills from army_data blocks.

## Connections
- [[PreventiveGuards]] — module under test
- [[GameState]] — state object being modified
- [[NarrativeResponse]] — schema for structured LLM output
- [[CoreMemories]] — concept for turn anchoring

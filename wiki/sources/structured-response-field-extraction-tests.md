---
title: "Structured Response Field Extraction Tests"
type: source
tags: [testing, python, unit-test, structured-data, schema]
source_file: "raw/structured-response-field-extraction-tests.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests for structured response field extraction and processing, validating the schema defined in game_state_instruction.md. Tests cover narrative containing session headers and planning blocks, debug_info with dice rolls and resources, and state_updates with NPC data.

## Key Claims
- **Required Fields**: Response must contain narrative, entities_mentioned, location_confirmed, state_updates, and debug_info
- **Debug Info Structure**: debug_info must contain dice_rolls (list), resources (string), dm_notes, and state_rationale
- **Session Header**: Narrative contains [SESSION_HEADER] marker with character info (level, HP, XP, gold)
- **Planning Block**: Narrative contains --- PLANNING BLOCK --- marker with formatted choice options
- **State Updates Structure**: state_updates contains npc_data with individual NPC state like goblin_1 HP

## Key Quotes
> "narrative should contain session header marker"
> "dice_rolls should be a list"
> "state_updates should contain npc_data"

## Connections
- [[StructuredResponseSchema]] — the schema being tested
- [[SessionHeader]] — character state component in narrative
- [[PlanningBlock]] — decision prompt component in narrative
- [[DebugInfo]] — debug metadata container

## Contradictions
- None identified

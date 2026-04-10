---
title: "Structured Response Schema"
type: concept
tags: [schema, structured-data, api, llm-response]
sources: []
last_updated: 2026-04-08
---

## Summary
The structured response schema defines the JSON format for LLM responses in the game system. It specifies required fields that must be present in every structured response from the language model.

## Key Components

### Required Fields
- **narrative**: The main story text, optionally containing [SESSION_HEADER] and --- PLANNING_BLOCK --- markers
- **entities_mentioned**: List of entity names referenced in the response
- **location_confirmed**: Confirmed location from the response
- **state_updates**: Dictionary containing game state changes (e.g., npc_data with HP values)
- **debug_info**: Container for debug metadata including dice_rolls, resources, dm_notes, state_rationale

### Debug Info Sub-fields
- **dice_rolls**: List of dice roll strings (e.g., "Attack roll: 1d20+5 = 20")
- **resources**: String describing character resources (HP, HD, action surge, etc.)
- **dm_notes**: List of DM-facing notes about decision rationale
- **state_rationale**: Explanation of why state changes were made

## Related Concepts
- [[SessionHeader]] — character state displayed in narrative
- [[PlanningBlock]] — player choice prompt in narrative
- [[StateUpdates]] — game state mutation from LLM response
- [[DebugInfo]] — debug metadata container

## Usage
Used by structured_fields_utils.extract_structured_fields to parse LLM responses into component parts for storage and display.

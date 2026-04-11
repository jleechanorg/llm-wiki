---
title: "Action Resolution Dice Roll Extraction Helper Functions"
type: source
tags: [action-resolution, dice-rolls, audit-events, world-logic, code-centralization]
source_file: "raw/action-resolution-dice-roll-extraction-helpers.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python helper functions that centralize logic for extracting and formatting dice rolls from action_resolution/outcome_resolution data structures. Eliminates duplication between llm_response.py and world_logic.py by providing unified extract_dice_rolls_from_action_resolution and extract_dice_audit_events_from_action_resolution functions.

## Key Claims
- **Centralization**: Single source of truth for action_resolution field access across llm_response.py and world_logic.py
- **Dice Roll Formatting**: Converts structured roll objects to display strings ("notation = total (purpose)")
- **DC/Success Tracking**: Handles difficulty class and success/failure status in roll formatting
- **Audit Event Extraction**: Extracts audit_events from mechanics for dice telemetry

## Key Quotes
> "Helper functions for action_resolution/outcome_resolution handling. Centralizes the logic for accessing and building action_resolution/outcome_resolution fields across llm_response.py and world_logic.py to eliminate duplication."

## Connections
- [[WorldLogic]] — consumer of extracted dice roll data
- [[LLMResponse]] — producer of action_resolution data
- [[DiceAudit]] — audit event processing system

## Contradictions
- None detected

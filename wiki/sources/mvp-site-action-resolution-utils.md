---
title: "Action Resolution Utils"
type: source
tags: [action-resolution, dice-rolls, audit, backward-compat]
sources: []
last_updated: 2026-04-14
---

## Summary

Centralized helper functions for action_resolution/outcome_resolution field handling across llm_response.py and world_logic.py. Eliminates duplication by providing a single access point for extracting dice rolls, audit events, and normalization logic. Also provides backward compatibility between legacy outcome_resolution field and the newer action_resolution field.

## Key Claims

- **Dice Roll Extraction**: `extract_dice_rolls_from_action_resolution()` converts structured roll objects into formatted display strings with format "notation = total (purpose)" or "notation = total vs DC dc - Success/Failure (purpose)"
- **Audit Event Extraction**: `extract_dice_audit_events_from_action_resolution()` extracts audit events from mechanics.audit_events, handling both dict and string formats
- **Backward Compatibility**: `get_action_resolution()` checks action_resolution first (new field), falls back to outcome_resolution (legacy field) for backward compatibility
- **Normalization**: `normalize_action_resolution_rolls()` fixes missing totals from result/rolls and maps 'label' to 'purpose' for frontend compatibility
- **Existence Check**: `has_action_resolution_dice()` returns True if mechanics has rolls or audit_events

## Key Quotes

> "Converts structured roll objects from action_resolution.mechanics.rolls into formatted strings for the legacy dice_rolls field (for UI display)"

> "Check action_resolution first (new field), falls back to outcome_resolution (legacy field) for backward compatibility"

> "The frontend expects 'purpose' but code execution may produce 'label'"

## Connections

- [[ActionResolution]] — related concept for action resolution mechanics
- [[AttackRoll]] — dice rolling is part of attack resolution
- [[DiceStrategy]] — may interact with dice strategy selection

## Contradictions

- None identified
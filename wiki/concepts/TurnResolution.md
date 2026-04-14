---
title: "TurnResolution"
type: concept
tags: [combat, action-resolution, dice-rolls, audit, game-logic]
sources: [mvp-site-action-resolution-utils, mvp-site-combat, mvp-site-upkeep]
last_updated: 2026-04-14
---

## Summary

The process of resolving a single combat turn in WorldAI — encompassing dice roll extraction, audit event capture, damage calculation with position multipliers, and post-turn upkeep deduction. Centralized via `get_action_resolution()` which falls back from `action_resolution` (new) to `outcome_resolution` (legacy) for backward compatibility.

## Key Claims

### Dice Roll Extraction
- `extract_dice_rolls_from_action_resolution()` converts structured roll objects to display strings
- Format: `"notation = total (purpose)"` or `"notation = total vs DC dc - Success/Failure (purpose)"`
- Handles missing totals and 'label' → 'purpose' mapping for frontend compatibility

### Audit Event Capture
- `extract_dice_audit_events_from_action_resolution()` pulls mechanics.audit_events
- Handles both dict and string formats for cross-version compatibility

### Damage Calculation (from [[mvp-site-combat]])
- Position multipliers: ranged=1.0x, melee=1.5x, flying=2.25x
- School counter bonuses applied after position multipliers
- Morale rout triggers when remaining HP <= MORALE_ROUT_THRESHOLD

### Backward Compatibility
- `get_action_resolution()` checks action_resolution first, falls back to outcome_resolution
- `has_action_resolution_dice()` returns True if mechanics has rolls or audit_events

## Connections

- [[ActionResolution]] — field-level action resolution mechanics
- [[AttackRoll]] — dice rolling for attack resolution
- [[CombatState]] — turn resolution produces combat state
- [[UpkeepPhase]] — time advancement triggers upkeep deduction
- [[mvp-site-action-resolution-utils]] — implementation utilities
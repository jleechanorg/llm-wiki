---
title: "ActionProcessing"
type: concept
tags: [action-resolution, dice-rolls, audit, turn-resolution, game-logic]
sources: [mvp-site-action-resolution-utils, mvp-site-combat, mvp-site-upkeep]
last_updated: 2026-04-14
---

## Summary

The end-to-end pipeline for processing player actions in WorldAI combat and world interactions. Encompasses dice roll extraction, audit event capture, damage calculation with position multipliers, combat state updates, and post-turn upkeep deduction. Centralized via `get_action_resolution()` for backward compatibility between action_resolution (new) and outcome_resolution (legacy) fields.

## Key Claims

### Action Resolution Pipeline
1. Dice roll execution (via dice.py or code_execution)
2. Structured roll data stored in `action_resolution.mechanics.rolls`
3. Audit events captured in `mechanics.audit_events`
4. `extract_dice_rolls_from_action_resolution()` formats for display
5. `extract_dice_audit_events_from_action_resolution()` captures audit trail

### Normalization
- Missing totals fixed in result/rolls
- 'label' mapped to 'purpose' for frontend compatibility
- Both dict and string audit event formats handled

### Backward Compatibility
- `get_action_resolution()` checks action_resolution first
- Falls back to outcome_resolution if new field absent
- `has_action_resolution_dice()` detects dice presence in mechanics

## Connections

- [[TurnResolution]] — turn-level action processing
- [[ActionResolution]] — field-level action resolution
- [[DiceAuthenticity]] — dice must be genuine executed rolls
- [[UpkeepPhase]] — post-combat upkeep deduction
- [[mvp-site-action-resolution-utils]] — implementation utilities
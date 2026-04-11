---
title: "Dice Integrity Module Unit Tests"
type: source
tags: [python, testing, dice-integrity, tdd]
source_file: "raw/test_dice_integrity.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests for the dice_integrity module that validate missing field detection, error response handling, tool result application to action_resolution, and god mode response validation. Tests enforce that dice violations only log warnings, never trigger LLM reprompts.

## Key Claims
- **Missing Fields Detection**: Tests validate that dice_rolls and dice_integrity fields are flagged when missing based on require_dice_rolls and dice_integrity_violation flags
- **No Reprompt Logic**: Dice integrity violations only log warnings, never retry the LLM — the reprompt function was intentionally deleted
- **Error Response Handling**: Tool errors (e.g., missing dc_reasoning) do not count as valid dice results
- **Tool Result Application**: Tool results populate action_resolution.mechanics.rolls with roll totals, DCs, and success/failure status
- **Attack/Damage Expansion**: Attack tool results expand to include both attack and damage rolls in action_resolution
- **God Mode Validation**: Non-dict action_resolution is ignored in god mode validation

## Connections
- [[Dice Integrity]] — the module being tested
- [[NarrativeResponse Schema]] — the response structure being validated
- [[Action Resolution]] — mechanics field that receives roll data from tool results

---
title: "Action Resolution Utils Unit Tests"
type: source
tags: [python, testing, unittest, action-resolution, dice-mechanics]
source_file: "raw/action-resolution-utils-unit-tests.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest file testing helper functions in mvp_site.action_resolution_utils module. Tests extract_dice_rolls_from_action_resolution which parses dice roll data from action_resolution objects, handling various formats including single/multiple rolls, DC/success/failure states, and edge cases like empty arrays and missing fields.

## Key Claims
- **Dice Roll Extraction**: Function extracts formatted dice roll strings from action_resolution.mechanics.rolls array
- **DC and Success Handling**: Properly formats rolls with difficulty class (DC) and success/failure outcome
- **Multiple Roll Support**: Handles extraction of multiple rolls in a single action_resolution
- **Graceful Degradation**: Returns empty list for missing/null mechanics.rolls without raising exceptions
- **Test Coverage**: Covers 8 distinct test cases including edge cases and invalid input

## Key Quotes
> "1d20+5 = 22 (Attack)" — single roll format
> "1d20+149 = 313 vs DC 45 - Success (Stealth (Soul Siphon Deception))" — roll with DC and success

## Connections
- [[Action Resolution Backward Compatibility End-to-End Test]] — related end-to-end tests for same module
- [[Sovereign Protocol System]] — game system that uses action_resolution for mechanics

## Contradictions
- None identified

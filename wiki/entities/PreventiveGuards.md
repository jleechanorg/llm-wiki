---
title: "PreventiveGuards"
type: entity
tags: [module, testing, game-state]
sources: [preventive-guards-unit-tests]
last_updated: 2026-04-08
---

## Description
Python module (`mvp_site.preventive_guards`) containing the `enforce_preventive_guards` function that applies defensive transformations to LLM responses before they're processed by the game system.

## Responsibilities
- Extract god_mode_response from narrative when mode is MODE_GOD
- Infer and record core memories from dice rolls
- Track and update world time when missing
- Preserve location state across turns
- Checkpoint resource updates
- Autofill faction minigame units from army_data

## Test Coverage
[[PreventiveGuardsUnitTests]] validates 7 scenarios including fallback behavior and state preservation logic.

---
title: "Core Memories"
type: concept
tags: [memory, game-state, turn-anchoring]
sources: [preventive-guards-unit-tests]
last_updated: 2026-04-08
---

## Description
Turn-anchoring mechanism in custom_campaign_state that records key narrative moments from each turn. Core memories preserve significant actions, observations, or outcomes for context in future LLM calls.

## Trigger Conditions
Recorded when dice_rolls are present in the response, even without explicit state_updates. This ensures every action that involves randomness gets anchored in the campaign history.

## Implementation
Entries are strings (not structured objects) stored in custom_campaign_state.core_memories list. Each entry captures a narrative snippet like "sprint across the deck as arrows fly."

## Related
- [[PreventiveGuards]] records memories from dice rolls
- [[MemoryUtils]] provides similarity detection and budget-based selection
- [[MemoryBudgetAlignment]] ensures MAX_CORE_MEMORY_TOKENS stays within bounds

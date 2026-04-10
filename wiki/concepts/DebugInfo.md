---
title: "Debug Info"
type: concept
tags: [debugging, metadata, logging, structured-data]
sources: []
last_updated: 2026-04-08
---

## Summary
A container within the structured response schema that holds debug metadata including dice rolls, resource states, DM notes, and state change rationale.

## Sub-fields
- **dice_rolls**: List of dice roll descriptions (e.g., "Attack roll: 1d20+5 = 20")
- **resources**: String summarizing character resources (HD, Second Wind, Action Surge)
- **dm_notes**: List of DM-facing notes about LLM decision-making
- **state_rationale**: Explanation of state changes (e.g., "Reduced goblin HP from 11 to 3 due to 8 damage taken")

## Purpose
- Debugging: Trace why the LLM made specific decisions
- Audit: Verify dice rolls and state changes are legitimate
- DM Tools: Provide DM with insight into AI reasoning

## Related Concepts
- [[StructuredResponseSchema]] — parent schema containing debug_info
- [[DiceRolls]] — individual dice roll records
- [[StateRationale]] — explanation of state mutations

## Usage
Stored alongside narrative in Firestore for post-session analysis and debugging.

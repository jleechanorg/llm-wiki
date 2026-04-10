---
title: "Turn 1 Activation"
type: concept
tags: [agent-activation, invariant, character-creation]
sources: []
last_updated: 2026-04-08
---

## Description
Critical invariant in the campaign storytelling system: CharacterCreationAgent MUST activate on the first turn (Turn 1) regardless of any pre-existing character data from God Mode or templates.

## Why It Matters
Ensures users creating campaigns from templates like "My Epic Adventure" review and finalize their character before story mode begins. This prevents the system from jumping straight to SCENE 1 with pre-defined character data without user acknowledgment.

## Test Validation
E2E tests validate that CharacterCreationAgent activates on Turn 1 even when:
1. God Mode includes full character data (name, class, stats)
2. God Mode includes minimal character data (just name and setting)

## See Also
- [[CharacterCreationAgent]]
- [[GodMode]]
- [[CampaignCreation]]

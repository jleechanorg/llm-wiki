---
title: "Inventory Validation"
type: concept
tags: [validation, game-mechanics, worldarchitect]
sources: [game-state-management-protocol]
last_updated: 2026-04-08
---

Inventory Validation is a mandatory check that ensures players can ONLY use items present in their `equipment` slots or `backpack`. Claims to items not in game state must be rejected.

**Validation Rules**:
- Check player's `equipment` slots
- Check player's `backpack` inventory
- Reject claims to non-existent items
- Prevent invalid item usage in narrative

**Related Concepts**:
- [[GameStateExamples]] — validation rules reference
- [[EquipmentDisplayUtilities]] — equipment query detection
- [[VisibilityRule]] — state updates invisible to players

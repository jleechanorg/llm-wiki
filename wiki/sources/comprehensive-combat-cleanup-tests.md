---
title: "Comprehensive Combat Cleanup Tests"
type: source
tags: [python, testing, combat, automatic-cleanup, game-state]
source_file: "raw/test_comprehensive_combat_cleanup.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite validating the automatic combat cleanup system that removes defeated enemies from combatants, initiative order, and NPC data when their HP reaches zero through AI-driven state updates.

## Key Claims
- **HP-Based Defeat Detection**: Enemies with hp_current set to 0 are automatically removed from combat
- **Automatic Cleanup Workflow**: Defeated enemies are removed from combatants, initiative order, and NPC data
- **Living Entity Preservation**: PCs and allied NPCs remain intact after cleanup
- **State Update Integration**: Cleanup works through the update_state_with_changes → apply_automatic_combat_cleanup pipeline

## Key Test Cases
- Enemy defeated via AI HP update should trigger automatic cleanup
- Defeated enemy removed from combatants after HP=0 update
- Defeated enemy removed from initiative order
- Defeated enemy removed from NPC data
- Living entities (Hero, Merchant) should remain in state

## Connections
- [[GameState]] — manages combat state and combatants
- [[FirestoreService]] — provides update_state_with_changes function
- [[WorldLogic]] — provides apply_automatic_combat_cleanup function

## Contradictions
- None identified

---
title: "Level-Up Modal Routing Scenarios"
type: source
tags: [routing, modal, level-up, character-creation, state-machine]
source_file: "raw/level-up-modal-routing-scenarios.json"
sources: []
last_updated: 2026-04-08
---

## Summary
Test scenarios defining routing logic for level-up and character creation modals in a D&D 5e game interface. Covers four scenarios: pending activation, stale blocking, in-progress override, and creation lock priority.

## Key Claims
- **level_up_pending=true + valid XP**: Routes to LevelUpAgent modal with priority "3_modal_level_up"
- **explicit level_up_pending=false**: Blocks stale modal reactivation even when rewards_pending exists
- **level_up_in_progress=true**: Overrides pending=false, maintains modal active
- **character_creation_in_progress**: Takes routing priority over level-up, routes to CharacterCreationAgent

## Routing Priority Hierarchy
1. CharacterCreationAgent (when character_creation_in_progress=true)
2. LevelUpAgent (when level_up_in_progress=true OR level_up_pending=true with valid XP)
3. Other modals

## Scenarios
| Scenario | Trigger | Expected Modal |
|----------|---------|----------------|
| level_up_pending_activates_modal | pending=true, XP≥threshold | LevelUpAgent |
| stale_pending_false_blocks_modal | pending=false | None |
| in_progress_overrides_pending_false | in_progress=true | LevelUpAgent |
| char_creation_lock_has_priority | creation_in_progress=true | CharacterCreationAgent |

## Connections
- [[LevelUpAgent]] — handles the level-up flow modal
- [[CharacterCreationAgent]] — handles initial character creation modal
- [[LivingWorldTriggerEvaluation]] — related state-based trigger system
- [[LevelUpMode]] — D&D 5e level-up mechanics protocol

---
title: "Automatic Combat Cleanup"
type: concept
tags: [combat, game-mechanics, automation]
sources: [comprehensive-combat-cleanup-tests]
last_updated: 2026-04-08
---

System that automatically removes defeated enemies from combat when their HP reaches zero. Cleans up combatants list, initiative order, and NPC data.

## How It Works
1. AI sets enemy hp_current to 0 via state update
2. update_state_with_changes applies the HP change
3. apply_automatic_combat_cleanup detects HP=0 and removes entity from:
   - combat_state.combatants
   - combat_state.initiative_order
   - npc_data

## Related
- [[HP-BasedDefeatDetection]]
- [[GameState]]

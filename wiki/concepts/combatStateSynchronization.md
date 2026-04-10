---
title: "Combat State Synchronization"
type: concept
tags: [game-state, combat, synchronization, npc]
sources: [npc-death-state-persistence-e2e-tests]
last_updated: 2026-04-08
---

## Description
The process of maintaining consistency between combat_state (active combatants) and npc_data (persistent NPC registry) when NPC states change during combat.

## Synchronization Points
1. When NPC dies: Remove from combat_state.combatants, update npc_data status
2. When NPC enters combat: Add to combat_state.combatants, reference npc_data
3. When NPC is revived: Restore to combat_state, clear dead status in npc_data

## Connections
- [[combat_state]] — active combat tracking
- [[npc_data]] — NPC persistence layer
- [[NPC Death State Persistence]] — specific synchronization scenario

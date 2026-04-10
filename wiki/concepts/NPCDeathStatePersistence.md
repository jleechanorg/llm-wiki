---
title: "NPC Death State Persistence"
type: concept
tags: [game-logic, npc, state-management, synchronization]
sources: [npc-death-state-persistence-e2e-tests]
last_updated: 2026-04-08
---

## Description
The synchronization of NPC death state between combat_state and npc_data systems. When an NPC is killed in combat, the game must:

1. Remove the NPC from active combatants in combat_state
2. Preserve the NPC in npc_data with a dead status indicator
3. Prevent the dead NPC from being offered as targets in subsequent turns

## Problem
Bug: When a user kills an NPC (e.g., Marcus), the game still presents options to kill them again on subsequent turns. The death state is not being properly synced between combat_state and npc_data.

## Solution Path
- Test verifies full flow from API endpoint through all service layers
- Validates NPC is removed from combat but preserved in npc_data
- Ensures subsequent turns don't offer dead NPCs as targets

## Connections
- [[combat_state]] — tracks active combatants in current combat
- [[npc_data]] — persistent NPC registry with roles and descriptions
- [[NPC Death State Persistence E2E Tests]] — tests this synchronization

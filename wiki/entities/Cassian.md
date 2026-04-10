---
title: "Cassian"
type: entity
tags: [npc, player-reference, entity-instruction-test]
sources: [enhanced-explicit-entity-instructions-tests]
last_updated: 2026-04-08
---

Cassian is the player-referenced NPC in entity instruction tests. Marked as mandatory because the player specifically mentioned Cassian. Tests validate that player references trigger higher-priority entity requirements with direct narrative continuity enforcement.

**Key test appearances:**
- Player reference detection: player_references = ["Cassian"]
- Mandatory entity instruction type with priority=1
- "The player specifically mentioned Cassian" triggers mandatory requirement

**Related concepts:** [[EntityInstructionGenerator]], [[EntityEnforcementChecker]]

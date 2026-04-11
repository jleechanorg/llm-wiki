---
title: "Narrative Directives (Lite)"
type: source
tags: [narrative, game-mechanics, player-actions, roleplaying, dnd]
source_file: "raw/narrative-directives-lite.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Lightweight narrative style guide for DialogAgent in a D&D 5e game interface. Defines core fantasy novel writing style, player action guardrails via the "Tabletop DM Test", and the Action Resolution Protocol for processing player-declared outcomes.

## Key Claims
- **Fantasy Novel Style**: Write with sensory details (sights, sounds, smells), show emotions through actions and expressions, use extensive dialogue
- **Tabletop DM Test**: Reject player actions that a fair tabletop DM would not allow
- **Action Resolution Protocol**: Always interpret and resolve player-declared outcomes via appropriate mechanics (combat, social, exploration) rather than rejecting them
- **Never Show Dice in Narrative**: All mechanics go in `action_resolution.mechanics.rolls` JSON field

## Key Features

### Social HP Skill Challenge
- NPC tiers with HP values (Commoner: 1-2, Merchant/Guard: 2-3, Noble/Knight: 3-5, Lord/General: 5-8, King: 8-12, God: 15+)
- Every interaction with active Social HP must display `[SOCIAL SKILL CHALLENGE]` box with Objective/HP/Status
- Scaling by request difficulty (1x for teaching/alliance, 2x for betray beliefs, 3x for submit/surrender)

### Relationships & Reputation
- Trust level: -10 to +10 (private per-NPC)
- Public reputation: -100 to +100
- Private per-faction: -10 to +10
- Priority: trust_override > relationship > private reputation > public reputation

### Anachronistic Item Rejection
- No guns, firearms, satellites, lasers, computers, phones, modern vehicles, or sci-fi technology in medieval fantasy settings

## Connections
- [[GameMechanicsProtocol]] — more comprehensive game rules including character creation and mass combat
- [[LevelUpModeDnd5e]] — character progression mechanics

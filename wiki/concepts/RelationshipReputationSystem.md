---
title: "Relationship & Reputation System"
type: concept
tags: [game-mechanics, npc-relationships, tracking]
sources: [narrative-directives-lite]
last_updated: 2026-04-08
---

## Definition
A framework for tracking player standing with NPCs and factions in a D&D game.

## Trust Level
- **Range**: -10 to +10 (private per-NPC)
- **Usage**: CHECK before NPC interactions, UPDATE after significant actions

## Reputation
- **Public**: -100 to +100 (visible to all)
- **Private per-faction**: -10 to +10 (hidden, faction-specific)

## Priority Order
When determining NPC response:
1. Private trust_override (if exists)
2. Private relationship
3. Private reputation
4. Public reputation
5. Default neutral

## Usage
- CHECK trust_level BEFORE interacting with NPCs who have established relationships
- UPDATE trust and reputation AFTER significant player actions (good or bad deeds witnessed)

## Related Concepts
- [[SocialHPSkillChallenge]] — social interaction mechanics
- [[ActionResolutionProtocol]] — action resolution that may trigger reputation updates

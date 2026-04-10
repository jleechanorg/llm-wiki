---
title: "NPC Agenda"
type: concept
tags: [game-mechanics, npc-behavior, ai-behavior]
sources: [living-world-advancement-protocol]
last_updated: 2026-04-08
---

## Definition
The independent goals and motivations that NPCs pursue in the Living World system. NPCs are not passive - they have their own agendas that may align with, conflict with, or be independent of the player's wishes.

## NPC Behavior Principles
- NPCs pursue their own goals based on personality and motivations
- Characters given tasks by the player may succeed, fail, or deviate
- NPCs make independent decisions without player input
- Allied NPCs may take initiative without orders
- Enemy NPCs prepare, scheme, or move against the player

## Implementation
NPC agendas are expressed through [[BackgroundEvent]] entries where:
- `actor` is the NPC name
- `action` describes what they did to pursue their goal
- `outcome` shows the result (success, failure, or ongoing)
- `event_type` indicates immediate or long-term impact

## Player Interaction
NPC agendas create emergent narrative through:
- Parallel storylines the player may discover
- Consequences of NPC decisions affecting player quests
- Opportunities for player to influence NPC goals
- Conflicts between NPC agendas creating world tension
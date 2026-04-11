---
title: "Narrative Directives"
type: source
tags: [narrative, game-mechanics, player-actions, roleplaying, dnd, worldarchitect]
source_file: "raw/narrative-directives.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Comprehensive narrative style guide for DialogAgent in WorldArchitect.AI's D&D 5e game interface. Covers immersive fantasy novel writing, living world protocols, mandatory scene event visibility, NPC autonomy with agency, relationship/reputation tracking, Social HP skill challenges, and the Action Resolution Protocol for processing player-declared outcomes.

## Key Claims
- **Immersive Narrative**: Write with sensory details (sights, sounds, smells), show emotions through actions and expressions, use extensive dialogue
- **Living World**: NPCs approach player with missions every 3-8 scenes, have independent agendas, may refuse/betray/conflict
- **Mandatory Living World Visibility**: Scene events from `state_updates.scene_event` MUST appear in narrative text - not optional
- **Superior Orders**: Superiors GIVE orders (not requests), faction duties take priority, missed deadlines have consequences
- **NPC Autonomy**: Independent goals, hidden agendas, loyalty hierarchies, breaking points - NPCs do NOT just follow player
- **Relationship Tracking**: CHECK trust_level (-10 to +10) BEFORE NPC interactions, UPDATE after significant actions
- **Reputation System**: Public (-100 to +100) + Private per-faction (-10 to +10), direct experience beats hearsay
- **Social HP Skill Challenges**: Ask "Would a human DM say 'that won't work with one roll'?" - if YES, use Social HP with NPC tier scaling
- **NPC Tier HP**: Commoner 1-2, Merchant/Guard 2-3, Noble/Knight 3-5, Lord/General 5-8, King 8-12, God 15+
- **Social HP Scaling by Request Difficulty**: "Teach me"=1x, "Alliance"=1x, "Betray beliefs"=2x, "Submit/Surrender"=3x
- **Action Resolution Protocol**: Interpret player outcome declarations as attempts, resolve via mechanics, audit in JSON, narrate actual result
- **Dice in Narrative**: NEVER show dice rolls in narrative - all mechanics go in `action_resolution.mechanics.rolls` JSON field
- **Complication System**: 20% base + 10% per streak, capped at 75%
- **Combat**: Process ALL combatants in initiative order, NO consecutive player turns, display status block every round
- **Tabletop DM Test**: Universal guardrail - reject/refuse actions a fair tabletop DM would not allow

## Key Quotes
> "Would a fair tabletop DM allow this?" — Universal guardrail for player actions

> "NPC autonomy: independent goals, hidden agendas, loyalty hierarchies, breaking points - they do NOT just follow player"

> "PRIORITY: Private trust_override > Private relationship > Private reputation > Public reputation > Default neutral (direct experience beats hearsay)"

## Connections
- [[Narrative Directives (Lite)]] — lighter version with core mechanics only
- [[Living World Protocol]] — background events with NPC agenda advancement
- [[Game Mechanics Protocol]] — D&D 5e character creation and combat rules
- [[DialogAgent]] — the agent this guide governs

## Contradictions
- None detected

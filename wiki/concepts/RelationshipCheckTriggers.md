---
title: "Relationship Check Triggers"
type: concept
tags: [game-mechanics, npc-relationships, triggers, dnd]
sources: ["relationship-mechanics-detailed"]
last_updated: 2026-04-08
---

## Description
Mandatory validation events that require checking NPC relationship data BEFORE any interaction.

## Required Check Situations

1. **Player speaks to an NPC they've met before**
   - Look up trust_level and disposition
   - Review history, debts, grievances

2. **Player asks an NPC for help, information, or resources**
   - Apply [[Relationship Behavior Modifiers]]
   - Adjust DC for social checks

3. **Player returns to a location with known NPCs**
   - Check all NPCs at location
   - Update behavior accordingly

4. **Combat situation involving known NPCs**
   - Determine NPC's likely side
   - Apply hostile/devoted modifiers

5. **Any negotiation, persuasion, or social encounter**
   - Apply trust-based DC adjustments
   - Determine available information sharing

## Data to Check
- `trust_level` (numeric -10 to +10)
- `disposition` (categorical)
- `history` array (past interactions)
- `debts` array (owed and owing)
- `grievances` array (insults, betrayals)

## Usage
This is MANDATORY per the game design. NPCs must have their relationship data checked before ANY interaction that could be affected by past interactions.

## Related Concepts
- [[Trust Level Scale]] — Data values to check
- [[Relationship Behavior Modifiers]] — What to apply based on check
- [[Relationship Update Triggers]] — When to modify relationship data

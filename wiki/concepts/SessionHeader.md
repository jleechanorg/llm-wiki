---
title: "Session Header"
type: concept
tags: [ui, display, character-state, narrative]
sources: []
last_updated: 2026-04-08
---

## Summary
A structured display block within the narrative that shows the player's current character state including level, class, HP, XP, gold, resources, conditions, and other status information.

## Structure
The session header appears as a marked section in the narrative:
```
[SESSION_HEADER]
Timestamp: 1492 DR, Ches 20, 10:00
Location: Goblin Cave
Status: Lvl 2 Fighter | HP: 15/18 (Temp: 0) | XP: 450/900 | Gold: 25gp
Resources: HD: 2/2 | Second Wind: 0/1 | Action Surge: 1/1
Conditions: None | Exhaustion: 0 | Inspiration: No | Potions: 1
```

## Displayed Information
- **Timestamp**: In-game date and time
- **Location**: Current location
- **Status**: Level, class, HP (with temp), XP, gold
- **Resources**: Hit dice,Second Wind, Action Surge, potions
- **Conditions**: Active conditions, exhaustion level, inspiration, potions

## Related Concepts
- [[StructuredResponseSchema]] — parent schema containing session header
- [[PlanningBlock]] — companion block for player decisions
- [[CharacterState]] — the underlying state being displayed

## Usage
Extracted from narrative by structured_fields_utils and displayed in the game UI to keep players informed of their current status.

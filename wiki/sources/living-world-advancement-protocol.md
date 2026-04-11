---
title: "Living World Advancement Protocol"
type: source
tags: [living-world, game-mechanics, npc-behavior, faction-system, event-generation]
source_file: "raw/living-world-advancement-protocol.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Protocol for advancing the game world between player turns, generating background events showing NPC activities, faction movements, and world changes that occur independently of the player's current scene. Requires mandatory inclusion of `world_events` in state updates.

## Key Claims
- **World does NOT pause**: Living world advances during player turns with background events, off-screen NPC actions, and faction movements
- **Scene Event Visibility**: Scene events generated in `state_updates` must be rendered in player narrative the same turn
- **Background Event Structure**: 3 immediate events (player-visible within 1-2 turns) + 1 long-term event (5-15 turns later)
- **Player-Facing Opacity**: Living World mechanics are invisible - do not mention "Living World turn" in planning blocks
- **NPC Agenda Advancement**: NPCs pursue independent goals, may succeed/fail/deviate from player wishes

## Event Types

### Immediate Events (3 required)
Must have strong discovery hooks:
- Affects player's current location
- Impacts player's active mission
- NPC in current scene reacts to it
- Environmental change visible now

### Long-Term Event (1 required)
- Faction leadership changes
- Enemy preparations (10+ turns)
- Alliance formations or betrayals
- Resource accumulation/depletion

## Player-Aware Rules
- `player_aware: false` events must NOT appear in narrative
- Only reveal through natural narrative triggers
- Events are "just things that happen" from player perspective

## State Delta Format
```json
"world_events": {
  "background_events": [
    {
      "actor": "NPC Name",
      "action": "What they did",
      "location": "Where it happened",
      "outcome": "Result of their action",
      "event_type": "immediate|long_term",
      "status": "pending|discovered|resolved",
      "player_aware": true or false,
      "discovery_condition": "How/when player learns of this",
      "estimated_discovery_turn": null or turn_number
    }
  ]
}
```

## Contradictions
None identified - this protocol complements existing game state management without conflicting with prior sources.
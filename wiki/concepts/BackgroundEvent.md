---
title: "Background Event"
type: concept
tags: [game-mechanics, npc-behavior, world-simulation]
sources: [living-world-advancement-protocol]
last_updated: 2026-04-08
---

## Definition
An event representing NPC actions, faction movements, or world changes that occur off-screen, independent of the player's current scene. Generated in the `world_events.background_events` array.

## Structure
```json
{
  "actor": "NPC Name",
  "action": "What they did",
  "location": "Where it happened",
  "outcome": "Result of their action",
  "event_type": "immediate|long_term",
  "status": "pending|discovered|resolved",
  "player_aware": true or false,
  "discovery_condition": "How/when player learns",
  "estimated_discovery_turn": turn_number or null
}
```

## Event Types

### Immediate Events (3 per turn)
Must have strong discovery hooks affecting the player's immediate context:
- Affects current location (guards appear, prices change)
- Impacts active mission (road blocked, deadline moved)
- NPC in scene reacts to it during this turn
- Environmental change visible now (smoke, refugees)

### Long-Term Event (1 per turn)
Major faction/plot progression with delayed discovery:
- Faction leadership changes
- Enemy preparations (10+ turns)
- Alliance formations or betrayals
- Resource accumulation/depletion

## Discovery Conditions
- **Immediate**: Player learns within 1-2 turns through narrative triggers
- **Long-Term**: Player learns in 5-15 turns or never; discovery should be realistic (rumors, visible consequences)

## Player-Aware Flag
- `player_aware: true`: Event can be revealed in narrative
- `player_aware: false`: Must NOT appear in narrative - events are "just things that happen"
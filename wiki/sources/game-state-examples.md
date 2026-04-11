---
title: "Game State Examples"
type: source
tags: [dnd, game-state, response-format, session-header, validation]
source_file: "raw/game-state-examples.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Reference documentation for LLM response formatting in WorldArchitect.AI, covering session header requirements, response JSON schemas, inventory validation rules, and spell slot verification. Ensures consistent player state communication and prevents invalid item/spell usage.

## Key Claims
- **Session Header Required**: Every response (except DM MODE) must include `[SESSION_HEADER]` prefix with timestamp, location, status line, and optional resources
- **String Format Only**: session_header must be a STRING, not a JSON object
- **Inventory Validation**: Players can only use items in their `equipment` slots or `backpack` — reject claims to non-existent items
- **Spell Slot Logic**: Track available spell slots per level; reject casting if slots exhausted; implement upcasting validation
- **Dice Tool Requests**: Combat phases use tool_requests array for dice rolls with attack_modifier, target_ac, damage_notation, and purpose
- **Planning Block**: Every response includes planning_block with thinking, context, and choices for player decision-making

## Session Header Format
### Required Fields
- `[SESSION_HEADER]` prefix (mandatory)
- Timestamp in format: `[Year] DR, [Month] [Day], HH:MM:SS
- Location: current location name
- Status: Level, HP, XP, Gold formatted line
- Resources (optional): HD, Spells, Ki, Rage, Potions, Exhaustion

### Examples
```
[SESSION_HEADER]
Timestamp: 1492 DR, Mirtul 15, 14:30:00
Location: Moonrise Towers
Status: Lvl 5 Fighter | HP: 68/68 (Temp: 0) | XP: 1200/6400 | Gold: 150gp
Conditions: None | Exhaustion: 0 | Inspiration: No
Resources: HD: 5/8 | Spells: L1 4/4, L2 3/3 | Action Surge: 1/1
```

## Response Format Schema
### Combat Phase (with tool_requests)
```json
{
    "session_header": "[SESSION_HEADER]\nTimestamp: ...",
    "resources": "HD: 2/3, Spells: L1 2/2, ...",
    "narrative": "Afternoon ... — description of action",
    "tool_requests": [{"tool": "roll_attack", "args": {...}}],
    "planning_block": {"thinking": "...", "context": "...", "choices": {...}},
    "dice_rolls": [],
    "dice_audit_events": [],
    "entities_mentioned": ["..."],
    "location_confirmed": "...",
    "state_updates": {}
}
```

### Non-Combat Example
```json
{
    "session_header": "[SESSION_HEADER]\nTimestamp: ...",
    "resources": "...",
    "narrative": "...",
    "planning_block": {"thinking": "...", "context": "...", "choices": {...}},
    "dice_rolls": [],
    "dice_audit_events": [],
    "entities_mentioned": ["..."],
    "location_confirmed": "...",
    "state_updates": {}
}
```

## Inventory Validation Rules
### Critical Constraint
Players can ONLY use items that exist in their `equipment` slots or `backpack`. The LLM must:
1. Check game_state.equipment for equipped items
2. Check game_state.backpack/consumables for carried items
3. Reject claims to non-existent items with in-character narrative

### Correction Examples
| Player Claim | Reality | LLM Response |
|-------------|---------|---------------|
| "I attack with +3 Flaming Sword" | Only has Longsword +1 | "You draw your Longsword +1—though not the legendary blade you perhaps wished for—and strike!" |
| "I use my Scroll of Fireball" | No scroll in pack | "You reach for a scroll but find none in your pack." |
| "I pull Vorpal Sword from scabbard" | No vorpal sword | "You grasp at your scabbard, but no vorpal blade answers your call." |

## Spell Validation Rules
### Slot Tracking
- Track available slots per spell level
- Reject casting when slots exhausted
- Implement upcasting logic: higher-level slot for lower-level spell

### Upcasting Example
| Player Input | State | Correct Response |
|-------------|-------|-------------------|
| "Cast Healing Word" (No L1, has L2) | L1: 0/2, L2: 1/2 | "STOP AND ASK: You've exhausted your 1st-level power. You still have 2nd-level slots." |

## Connections
- [[DiceMechanics]] — tool_requests for combat dice rolling
- [[GameStateSchema]] — equipment/backpack structure for validation
- [[SessionHeader]] — session header format specification
- [[PlanningBlock]] — player choice presentation framework

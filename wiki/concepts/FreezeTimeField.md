---
title: "Freeze Time Field"
type: concept
tags: [game-mechanics, time-mechanics, meta-game]
sources: []
last_updated: 2026-04-08
---

## Definition
The freeze_time field is an optional boolean property on planning block choices that controls time advancement behavior. When freeze_time=true, selecting that choice advances game time by only 1 microsecond (similar to Think Mode), rather than advancing normally.

## Use Cases
- **Level-up decisions**: Meta-game choices that don't represent in-game time passing
- **Faction planning**: Strategic decisions outside normal time flow
- **Character development**: Background choices that occur instantaneously

## Behavior
| freeze_time Value | Time Advancement |
|-------------------|-----------------|
| true | 1 microsecond (minimal) |
| false | Normal advancement |
| missing | Normal advancement (default) |

## Related Concepts
- [[PlanningBlock]] — container for freeze_time field
- [[TurnAdvancementMechanics]] — how time progresses in normal gameplay
- Think Mode — another mechanism for minimal time advancement
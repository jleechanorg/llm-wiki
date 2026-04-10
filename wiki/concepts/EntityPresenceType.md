---
title: "EntityPresenceType"
type: concept
tags: [enum, entity-tracking, narrative, classification]
sources: []
last_updated: 2026-04-08
---

## Definition
Enum defining four distinct states of entity presence in narrative text for the WorldArchitect.AI game system.

## Enum Values
- **PHYSICALLY_PRESENT**: Entity is actively in the scene and participating
- **MENTIONED_ABSENT**: Entity is talked about but not physically present
- **IMPLIED_PRESENT**: Entity should be there based on narrative context
- **AMBIGUOUS**: Unclear whether entity is present or referenced

## Purpose
Enables precise tracking of entity states for narrative consistency, allowing the system to distinguish between entities that are actively in play versus those referenced in dialogue or absent from the scene.

## Related Concepts
- [[EntityContext]] — carries presence_type in entity metadata
- [[NarrativeSyncValidator]] — uses presence types for validation
- [[ContinuityChecking]] — monitors presence type changes across turns

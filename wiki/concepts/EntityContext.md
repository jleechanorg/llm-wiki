---
title: "EntityContext"
type: concept
tags: [dataclass, entity-tracking, narrative, context]
sources: []
last_updated: 2026-04-08
---

## Definition
Dataclass storing comprehensive contextual information about an entity in the narrative, including presence type, location, last action, emotional state, and physical markers.

## Fields
- **name**: Entity identifier
- **presence_type**: EntityPresenceType enum value
- **location**: Current scene location (optional)
- **last_action**: Most recent action taken (optional)
- **emotional_state**: Current emotional state (optional)
- **physical_markers**: List of visible physical traits (e.g., "bandaged ear", "trembling")

## Purpose
Maintains state continuity for entities across narrative generations, enabling the validator to detect when physical markers or emotional states change without explanation.

## Related Concepts
- [[EntityPresenceType]] — presence classification
- [[ContinuityChecking]] — validates physical marker consistency
- [[EmotionalStatePatterns]] — detects emotional states in narrative

---
title: "Entity Status Tracking"
type: concept
tags: [entity-tracking, state-management, game-mechanics]
sources: [entity-tracking-system]
last_updated: 2026-04-08
---

## Definition
The system of classifying entities by their current state in the narrative flow. Three statuses:
- **active**: Currently present and relevant to the scene
- **inactive**: Not currently present but known to exist
- **mentioned**: Referenced in dialogue or narrative but not currently active

## Purpose
Enables AI narrative generation to maintain awareness of which entities should be included or acknowledged in each scene, preventing orphaned characters or forgotten NPCs.

## Related
- [[Scene Manifest]] — container holding status-tracked entities
- [[Visibility Management]] — orthogonal dimension for entity state
- [[Entity Tracking System]] — module implementing this concept

---
title: "Visibility Management"
type: concept
tags: [entity-tracking, narrative, scene-management]
sources: [entity-tracking-system]
last_updated: 2026-04-08
---

## Definition
System for tracking where entities exist relative to the current scene's perspective. Three visibility states:
- **visible**: Currently in the scene and perceivable
- **hidden**: Present but not currently perceivable (e.g., hiding, invisible)
- **off-screen**: Not in the current location but known to exist

## Purpose
Complements entity status tracking by adding spatial awareness. Allows narrative generation to reference entities that exist but aren't currently in view, enabling dramatic reveals or off-screen events.

## Related
- [[Entity Status Tracking]] — orthogonal state classification
- [[Scene Manifest]] — container for visibility-tracked entities
- [[Dual-Mode Campaign System]] — may use visibility for faction location tracking

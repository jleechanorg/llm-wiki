---
title: "Entity Preloading"
type: concept
tags: [entity-preloading, prompt-engineering]
sources: [entity-preloading-system-tests]
last_updated: 2026-04-08
---

## Description
Prompt engineering technique that injects entity information into LLM context before generation. Ensures entities don't disappear from ongoing narratives by explicitly listing active player characters and NPCs with their current state.

## Implementation Options
- Option 3: Entity Pre-Loading System using EntityPreloader class
- Includes caching mechanism to avoid redundant generation
- Supports location-aware filtering for scene-specific entity injection

## Related Concepts
- [[EntityManifest]] — data structure holding entity state
- [[EntityPreloader]] — main class implementing preloading
- [[LocationEntityEnforcer]] — location-specific filtering

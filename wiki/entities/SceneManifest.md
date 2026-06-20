---
title: "SceneManifest"
type: entity
tags: [python, entity-tracking, game-state, manifest]
sources: [entity-preloader-backward-compatibility-shim]
last_updated: 2026-04-08
---

## Description
Game state structure containing all entities present in a scene. Produced by entity preloading/tracking system and passed to AI service for entity-aware story generation.

## Related
- [EntityTracking](EntityTracking.md) — module defining this class
- [EntityPreloader](EntityPreloader.md) — produces manifests
- [[CreateFromGameState]] — factory function

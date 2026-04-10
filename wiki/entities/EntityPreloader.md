---
title: "EntityPreloader"
type: entity
tags: [class, entity-preloading, caching]
sources: [entity-preloading-system-tests]
last_updated: 2026-04-08
---

## Description
Class responsible for generating entity manifests from game state and creating entity preload text for prompt injection. Supports caching to avoid redundant manifest generation.

## Key Methods
- `generate_entity_manifest(game_state, session_idx, story_idx)` — Creates entity manifest with caching
- `create_entity_preload_text(game_state, session_idx, story_idx, location=None)` — Generates preload text with optional location filter
- `get_entity_count(game_state, session_idx, story_idx)` — Returns entity counts dict

## Relationships
- Uses [[EntityManifest]] from entity_instructions module
- Called by story continuation pipeline to inject entity context
- Works with [[LocationEntityEnforcer]] for location-specific rules

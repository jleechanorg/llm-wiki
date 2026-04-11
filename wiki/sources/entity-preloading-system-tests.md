---
title: "Entity Pre-Loading System Tests"
type: source
tags: [python, testing, entity-preloading, caching, manifests]
source_file: "raw/test_entity_preloader.py"
last_updated: 2026-04-08
---

## Summary
Unit tests for Entity Pre-Loading System (Option 3) testing entity manifest generation and preload text creation. Tests cover EntityPreloader and LocationEntityEnforcer classes with caching, location-aware entities, and entity counting functionality.

## Key Claims
- **Entity Manifest Caching**: generate_entity_manifest() caches results to avoid redundant create_from_game_state calls
- **Preload Text Structure**: create_entity_preload_text() generates text with === ENTITY MANIFEST === header, PLAYER CHARACTERS PRESENT and NPCS PRESENT sections
- **HP Display**: Preload text shows current/max HP format (e.g., "HP: 25/30")
- **Location-Aware Entities**: Location-specific NPCs identified with "(resident)" suffix and personal furnishings note
- **Entity Counting**: get_entity_count() returns dict with player_characters, npcs, and total_entities keys

## Key Quotes
> "Do not let any of these entities disappear" — preload text enforces entity persistence requirement

## Connections
- [[EntityPreloader]] — core class generating entity manifests
- [[LocationEntityEnforcer]] — enforces location-specific entity rules
- [[EntityManifest]] — data structure containing player_characters and npcs lists

## Contradictions
- None identified

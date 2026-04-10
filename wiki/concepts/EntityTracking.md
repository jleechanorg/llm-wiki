---
title: "Entity Tracking"
type: concept
tags: [entity-tracking, production, game-state]
sources: [entity-tracking-production-implementation-tests, entity-tracking-budget-fix-end2end-test, entity-preloading-system-tests, generic-entity-tracking-tests]
last_updated: 2026-04-08
---

## Definition
Production implementation for tracking player characters and NPCs across game sessions. The system creates entity manifests from game state, generates preload text for context injection, and validates entity presence.

## Key Components
- **EntityManifest**: Data structure containing player_characters, npcs, scene_id, session_number, turn_number
- **EntityPreloader**: Generates entity manifests with caching and location-aware preloading
- **LocationEntityEnforcer**: Applies location-specific entity rules and constraints
- **EntityValidator**: Validates entity data integrity and requirements

## Entity ID Format
Entities use standardized ID format:
- Player Characters: `pc_[name]_<3-digit-number>` (e.g., `pc_gideon_001`)
- NPCs: `npc_[name]_<3-digit-number>` (e.g., `npc_sariel_001`)
- Scenes: `scene_s<session>_t<turn>[_<suffix>]` (e.g., `scene_s1_t5`)

## Known Issues
- Original bug: entity tracking tokens added AFTER context truncation but not budgeted in scaffold calculation
- Fix: ENTITY_TRACKING_TOKEN_RESERVE budgets ~3,500 tokens in scaffold calculation

## Connections
- [[EntityIDFormat]] — standardization pattern for entity IDs
- [[SceneManifest]] — per-scene entity data structure
- [[EntityTrackingBudget]] — token budgeting fix

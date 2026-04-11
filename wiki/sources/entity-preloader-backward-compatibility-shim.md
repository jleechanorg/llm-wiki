---
title: "Entity Preloader - Backward Compatibility Shim"
type: source
tags: [python, backward-compatibility, entity-tracking, entity-instructions, migration]
source_file: "raw/entity-preloader.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module maintained for backward compatibility. Re-exports EntityPreloader, LocationEntityEnforcer, SceneManifest, and related helpers from their consolidated locations in mvp_site.entity_instructions and mvp_site.entity_tracking. New code should import directly from mvp_site.entity_instructions.

## Key Claims
- **Backward Compatibility Shim**: Maintained to support existing imports while functionality moved to new locations
- **Re-Export Pattern**: Re-exports all public interfaces from entity_instructions and entity_tracking modules
- **Consolidation Target**: All new code should import EntityPreloader and LocationEntityEnforcer from mvp_site.entity_instructions

## Key Exports
- EntityPreloader: Entity instruction generator
- LocationEntityEnforcer: Location-based entity enforcement
- entity_preloader: Pre-configured singleton instance
- location_enforcer: Pre-configured location enforcer
- SceneManifest: Game state manifest structure
- create_from_game_state: Factory function for manifest creation

## Connections
- [[EntityInstructions]] — consolidated source for EntityPreloader/LocationEntityEnforcer
- [[EntityTracking]] — source for SceneManifest
- [[BackwardCompatibility]] — pattern this module implements

## Contradictions
- None — this module is purely transitional

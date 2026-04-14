---
title: "mvp_site entity_preloader"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/entity_preloader.py
---

## Summary
Backward compatibility shim module maintained for legacy imports. All functionality has been consolidated into entity_instructions.py. Import from mvp_site.entity_instructions for new code.

## Key Claims
- Re-exports EntityPreloader, LocationEntityEnforcer from entity_instructions
- Re-exports entity_preloader and location_enforcer global instances
- Re-exports SceneManifest and create_from_game_state from entity_tracking

## Connections
- [[EntityTracking]] — SceneManifest and create_from_game_state imported from entity_tracking
- [[mvpSiteEntityInstructions]] — consolidated functionality now lives here
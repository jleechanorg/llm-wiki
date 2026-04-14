---
title: "mvp_site narrative_sync_validator"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/narrative_sync_validator.py
---

## Summary
Narrative Synchronization Validator for production entity tracking. Delegates to EntityValidator for entity presence logic while adding narrative-specific features (emotional patterns, physical state detection). Prevents narrative desynchronization in production.

## Key Claims
- EntityPresenceType enum: PHYSICALLY_PRESENT, MENTIONED_ABSENT, IMPLIED_PRESENT, AMBIGUOUS
- EntityContext dataclass with presence, location, emotional_state, physical_markers
- NarrativeSyncValidator delegates to EntityValidator for core logic
- Emotional state patterns for narrative analysis

## Connections
- [[EntityTracking]] — production entity tracking validator
- [[EntityValidator]] — delegates to core entity validation

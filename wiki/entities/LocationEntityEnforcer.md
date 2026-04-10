---
title: "LocationEntityEnforcer"
type: entity
tags: [class, entity-tracking, location]
sources: [generic-entity-tracking-tests]
last_updated: 2026-04-08
---

Class enforcing entity requirements based on location. After refactoring, returns empty rules for all locations to avoid hardcoded campaign-specific mappings.

## Key Methods
- `get_required_entities_for_location()` - Returns empty dict {} for all locations

## Known Test Coverage
- [[Generic Entity TrackingTests]] - Tests for hardcoded location removal

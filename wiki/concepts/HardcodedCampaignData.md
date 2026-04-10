---
title: "Hardcoded Campaign Data"
type: concept
tags: [anti-pattern, software-engineering]
sources: [generic-entity-tracking-tests]
last_updated: 2026-04-08
---

Anti-pattern where system contains fixed references to specific campaigns or content that should be dynamic. Entity tracking originally had hardcoded references to Sariel campaign characters and locations.

## Problems
- System breaks when used with different campaigns
- Assumes knowledge of specific campaign structure
- Requires code changes to support new campaigns

## Solution
- [[GenericDesign]] approach with dynamic detection
- Remove hardcoded entity/location mappings
- Rely on runtime game state data

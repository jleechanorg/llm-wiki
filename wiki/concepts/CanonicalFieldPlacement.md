---
title: "Canonical Field Placement"
type: concept
tags: [schema, data-modeling, migration]
sources: [schema-enforcement-end2end-tests-rev-jgd8]
last_updated: 2026-04-08
---

## Description
The practice of storing data in its designated (canonical) location within the schema. The "gold standard" requires all new writes to use canonical field locations, with automatic backfill for legacy locations.

## Gold Standard Requirements
- New writes must use canonical field locations
- Legacy field locations are automatically migrated
- Validation ensures no invalid state reaches persistence

## Related
- [[GameState]] — enforces canonical placement
- [[SchemaEnforcement]] — validates correct placement

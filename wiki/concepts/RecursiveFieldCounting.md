---
title: "Recursive Field Counting"
type: concept
tags: [testing, validation, data-integrity]
sources: [sariel-test-files-analysis]
last_updated: 2026-04-08
---

## Description
Validation technique that recursively counts all fields in each entity type to track state evolution. Used in production_validation and exact_production tests.

## Purpose
- Track game state evolution across interactions
- Detect field loss or corruption
- Validate all entity types (player, NPC, world, combat)

## Implementation
- Counts nested fields recursively
- Groups by entity type
- Compares counts before/after interactions

## Connections
- [TestSarielProductionValidation](../entities/TestSarielProductionValidation.md) — primary user
- [TestSarielExactProduction](../entities/TestSarielExactProduction.md) — also uses it
- [GameStateValidation](GameStateValidation.md) — broader concept

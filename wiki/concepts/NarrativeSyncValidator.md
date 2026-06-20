---
title: "Narrative Sync Validator"
type: concept
tags: [validation, entity-tracking, sync]
sources: ["complete-combined-approach-tests"]
last_updated: 2026-04-08
---

## Description
Validation component that checks narrative output consistency with game state. Validates entity coverage and location confirmation.

## Key Methods
- validate_entity_coverage() — checks entity mentions
- location_confirmed validation
- Integration with NarrativeResponse schema

## Related Concepts
- [EntityCoverageValidation](EntityCoverageValidation.md) — specific validation type
- [NarrativeResponseSchema](NarrativeResponseSchema.md) — response structure
- [LLM-FirstStateManagement](LLM-FirstStateManagement.md) — broader pattern

## Test Coverage
- Full workflow test validates validator integration

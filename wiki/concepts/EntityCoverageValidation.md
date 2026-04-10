---
title: "Entity Coverage Validation"
type: concept
tags: [validation, entity-tracking, quality-assurance]
sources: ["complete-combined-approach-tests"]
last_updated: 2026-04-08
---

## Description
Post-generation validation step that checks if LLM mentioned all expected visible entities in narrative output. Part of Combined approach validation layer.

## Key Logic
- Compare entities_mentioned vs expected_entities
- Hidden entities excluded from expected list
- Generate missing entity warnings
- Integration with NarrativeSyncValidator

## Related Concepts
- [[StructuredGeneration]] — generation step
- [[NarrativeSyncValidator]] — validator implementation
- [[LLM-FirstStateManagement]] — broader pattern

## Test Coverage
- test_step3_entity_coverage_validation validates the logic

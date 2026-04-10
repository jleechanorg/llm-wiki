---
title: "REV-jgd8"
type: entity
tags: [pr, e2e-testing, schema-enforcement]
sources: [schema-enforcement-end2end-tests-rev-jgd8]
last_updated: 2026-04-08
---

## Description
Pull request introducing dedicated end-to-end tests for schema enforcement in the full request path. Tests validate that schema validation runs on every turn via GameState.to_validated_dict and verifies canonical field placement for new writes.

## Test Coverage
- End-to-end flow from Flask API through to Firestore persistence
- Schema validation enforcement via GameState.to_validated_dict
- Canonical field placement (gold standard) for new writes
- Legacy flat location backfill to canonical location
- Debug mode response validation

## Related
- [[SchemaEnforcementEnd2EndTests]] — source page for test implementation
- [[GameState]] — entity being validated

---
title: "Schema Enforcement"
type: concept
tags: [schema, validation, testing]
sources: [schema-enforcement-end2end-tests-rev-jgd8]
last_updated: 2026-04-08
---

## Description
Practice of ensuring all data written to the system conforms to a defined schema. In the game system, enforced via GameState.to_validated_dict which runs on every turn to validate canonical field placement and prevent invalid state mutations.

## Key Aspects
- **Every Turn Validation**: Schema validation runs on every game interaction
- **Canonical Field Placement**: Gold standard requires fields in expected locations
- **Legacy Backfill**: Old field locations automatically migrate to canonical form

## Related
- [[GameState]] — enforces schema on each turn
- [[REV-jgd8]] — E2E tests for schema enforcement

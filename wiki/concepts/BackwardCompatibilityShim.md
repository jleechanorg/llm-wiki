---
title: "Backward Compatibility Shim"
type: concept
tags: [software-pattern, migration, python]
sources: [entity-utils-backward-compatibility-shim]
last_updated: 2026-04-08
---

A software design pattern where a module re-exports functions from a new location to maintain support for legacy import paths. Allows gradual migration of codebases without requiring immediate updates to all existing imports.

**Key characteristics:**
- Re-exports public interfaces from new module location
- Maintains identical function signatures
- Serves as temporary migration aid
- New code should import directly from consolidated location

**Examples in codebase:**
- [[Entity Utils - Backward Compatibility Shim]] — re-exports from mvp_site.entity_validator
- [[Entity Preloader — Backward Compatibility Shim]] — re-exports from entity_instructions and entity_tracking

**Related:** [[Migration Strategy]], [[Module Consolidation]]

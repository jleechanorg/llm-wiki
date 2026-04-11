---
title: "Entity Utils - Backward Compatibility Shim"
type: source
tags: [python, backward-compatibility, entity-validation, migration]
source_file: "raw/entity-utils.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module maintained for backward compatibility. Re-exports two functions from the consolidated entity_validator module, allowing legacy code to continue importing from the old path while new code imports directly from mvp_site.entity_validator.

## Key Claims
- **Backward Compatibility Shim**: Maintains import paths for legacy code while functionality moved to entity_validator
- **Re-Export Pattern**: Exports filter_unknown_entities and is_unknown_entity from consolidated module
- **Migration Support**: Eases transition to new module structure without breaking existing imports

## Key Exports
- filter_unknown_entities: Filters entities that are not recognized by the validator
- is_unknown_entity: Checks if a given entity is unknown to the system

## Connections
- [[EntityValidator]] — the consolidated module this shim wraps
- [[Entity Tracking System]] — higher-level entity tracking that uses validation
- [[Backward Compatibility]] — the software pattern this module implements

## Contradictions
- None identified

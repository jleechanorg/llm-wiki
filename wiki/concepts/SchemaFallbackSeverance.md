---
title: "Schema Fallback Severance"
type: concept
tags: [architecture, schema-validation, regression, anti-pattern]
---

When adding strict schema validation for a field, removing the legacy fallback path without verifying the LLM has fully migrated to the new schema is a silent data-loss regression. The LLM may continue using the legacy field while the backend ignores it.

## Example

PR #5563 added strict `location_confirmed` extraction, severing the fallback to `world_data.location`. The LLM was still writing to `world_data.location` but the backend stopped reading it.

## Rule

Before removing any fallback path in `preventive_guards.py` or similar guards:
1. Grep for all code paths still producing the legacy field
2. Verify the LLM prompt contract requires the new field
3. If the legacy field is still used, the fallback must remain
4. Add a test that proves the fallback works when the new field is absent

## Related

- [[AdminOverrideContract]] — admin overrides that skip guards
- [[SchemaValidation]] — strict validation patterns
- [[ZeroFrameworkCognition]] — LLM decides, server executes; don't assume LLM compliance

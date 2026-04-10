---
title: "Dice Rolls Normalization"
type: concept
tags: [schema-migration, backward-compatibility, legacy-fields]
sources: [action-resolution-field-consolidation-tests]
last_updated: 2026-04-08
---

## Definition
The process of converting legacy fields (dice_rolls, dice_audit_events) into the modern action_resolution format. This ensures backward compatibility with older code while migrating to the consolidated schema.

## Normalization Behavior
- dice_rolls array → mechanics.rolls array
- dice_audit_events array → mechanics.audit_events array
- Adds "normalized_from_legacy" to audit_flags
- Does NOT override existing action_resolution if present

## Test Validation
The test suite verifies that:
1. Legacy fields are properly converted
2. normalized_from_legacy flag marks converted data
3. Existing action_resolution takes precedence

## Related Concepts
- [[ActionResolution]] — target schema
- [[BackwardCompatibility]] — design principle

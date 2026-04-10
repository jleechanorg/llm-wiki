---
title: "Audit Flags"
type: concept
tags: [audit, schema, tracking, compliance]
sources: [action-resolution-field-consolidation-tests]
last_updated: 2026-04-08
---

## Definition
An array field in action_resolution that tracks metadata about the action processing. Common values include "normalized_from_legacy" (for migrated data) and "player_declared_outcome" (when player specifies expected result).

## Default Behavior
- Defaults to empty list [] if not provided
- Non-empty values indicate special processing occurred

## Common Values
- "normalized_from_legacy" — data migrated from old schema
- "player_declared_outcome" — player explicitly stated expected result

## Related Concepts
- [[ActionResolution]] — parent field
- [[ReinterpretedField]] — related flag for reinterpretation tracking

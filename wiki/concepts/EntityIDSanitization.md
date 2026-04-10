---
title: "Entity ID Sanitization"
type: concept
tags: [entity-id, validation, pydantic]
sources: [entity-id-special-characters-validation]
last_updated: 2026-04-08
---

## Description
Process of converting entity display names to valid entity_id strings by removing or replacing special characters. Ensures entity IDs match Pydantic pattern `^npc_\w+$` or `^pc_\w+$`.

## Sanitization Rules
1. Apostrophes (') are removed
2. Non-alphanumeric characters are replaced with underscores or removed
3. Non-ASCII characters have unicode normalization applied
4. Consecutive spaces are collapsed to single underscore
5. Leading/trailing underscores are removed

## Related
- [[EntityIDValidation]] — the validation that IDs must match patterns
- [[PydanticValidation]] — the schema validation framework used

---
title: "Entity Name Sanitization"
type: concept
tags: [string-processing, identifiers, normalization]
sources: []
last_updated: 2026-04-08
---

## Description
The process of transforming entity names into valid identifier strings suitable for use as IDs, keys, or database identifiers. The `sanitize_entity_name_for_id` function implements this pattern.

## Transformation Rules
1. **Lowercase**: All characters converted to lowercase
2. **Space substitution**: Spaces become underscores
3. **Apostrophe collapse**: Multiple apostrophes reduce to single character
4. **Special characters**: @, #, $, %, &, *, !, ? → underscore or removed
5. **Unicode**: Latin accents normalized (é→e), non-Latin scripts removed
6. **Whitespace**: Leading/trailing/multiple spaces collapsed
7. **Consecutive special chars**: Collapse to single underscore

## Use Cases
- Generating valid Firebase document IDs for NPCs
- Creating safe entity keys for game state
- Normalizing user-provided names to consistent format

## Related
- [[LlMService]] — module containing the implementation
- [[UnicodeHandling]] — technical concept for unicode processing

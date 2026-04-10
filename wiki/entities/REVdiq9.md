---
title: "REV-diq9"
type: entity
tags: [revision, schema-validation, catch-all-bypass]
sources: []
last_updated: 2026-04-08
---

## Description
Revision identifier for schema validation fix that detects invalid player_character_data. Part of PR #4534.

## Purpose
The schema originally had a catch-all branch `{"type": "object", "minProperties": 1}` allowing any object like `{"garbage": true}` to pass validation. This fix removes the catch-all and ensures only valid PlayerCharacter structure or null is accepted.

## Related
- [[PR4534]] — Parent PR
- [[SchemaValidation]] — The validation system being fixed
- [[SchemaCatchAllBypass]] — The vulnerability this fixes

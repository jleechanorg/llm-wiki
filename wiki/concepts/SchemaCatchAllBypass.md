---
title: "Schema Catch-All Bypass"
type: concept
tags: [schema-validation, security, vulnerability, json-schema]
sources: []
last_updated: 2026-04-08
---

## Description
Vulnerability in JSON Schema where a catch-all branch like `{"type": "object", "minProperties": 1}` allows any arbitrary object to pass validation, bypassing intended type constraints.

## Example
```json
{"type": "object", "minProperties": 1}
```
This allows `{"garbage": true, "not_a_valid_field": "should fail"}` to pass when it should fail.

## Fix (REV-diq9)
Remove catch-all branches and enforce strict type definitions for player_character_data.

## Related
- [[REVdiq9]] — Revision fixing this vulnerability
- [[SchemaValidation]] — System this vulnerability existed in
- [[JSONSchemaValidation]] — The validation standard affected

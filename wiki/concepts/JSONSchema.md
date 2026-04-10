---
title: "JSON Schema"
type: concept
tags: [schema, validation, json]
sources: [schema-strictness-schema-coverage-guard-tests]
last_updated: 2026-04-08
---

JSON Schema is a vocabulary that allows annotating and validating JSON documents. Used in game_state.schema.json to define structured types with $ref references and explicit properties. The schema enforces strict typing and prevents invalid state mutations.

## Related
- [[GameStateSchema]] — concrete schema file
- [[SchemaStrictness]] — enforced via JSON Schema validation

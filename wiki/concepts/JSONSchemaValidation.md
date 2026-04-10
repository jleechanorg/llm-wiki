---
title: "JSON Schema Validation"
type: concept
tags: [validation, json-schema, runtime-validation, schema-driven]
sources: ["json-schema-validation-game-state"]
last_updated: 2026-04-08
---

## Summary
JSON Schema validation is a schema-driven approach to validating JSON data structures. In WorldAI, the GameState schema validation module uses Draft202012Validator to validate runtime game state against the canonical game_state.schema.json.

## Key Components
- **Validator Compilation**: JSON Schema compiled to validators for efficient reuse
- **Format Checking**: Custom format validators (e.g., RFC 3339 datetime)
- **Caching**: In-memory caching of both schemas and compiled validators
- **Error Enrichment**: Adding user-actionable context to validation failures

## Usage
The validation module is used to:
1. Validate incoming game state updates
2. Verify data integrity on load
3. Provide meaningful error messages for invalid state

## Related
- [[GameStateSchema]] — the canonical schema being validated
- [[ValidationModule]] — broader validation context
- [[ADR0003]] — architectural decision

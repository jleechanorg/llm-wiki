---
title: "Runtime-generated Pydantic Models"
type: source
tags: [python, pydantic, json-schema, code-generation, dynamic-models]
source_file: "raw/runtime-generated-pydantic-models.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Runtime-generated Pydantic models from the canonical JSON Schema. The JSON Schema (game_state.schema.json) is the SINGLE source of truth, with Pydantic models generated dynamically at import time to guarantee they never diverge from the schema. Real validation is performed by validate_game_state() via jsonschema; this Pydantic model exists for to_model()/from_model() round-trip serialization support only.

## Key Claims
- **Single Source of Truth**: JSON Schema (game_state.schema.json) is the authoritative source for game state structure
- **Dynamic Generation**: Pydantic models are generated at runtime, not statically, eliminating schema drift
- **Dual Validation**: Pydantic model uses extra='allow' for round-trip serialization; real validation via jsonschema
- **Historical Fix**: Previously static models (1100+ lines) diverged from schema over time — dynamic approach eliminates this

## Key Quotes
> "Uses extra='allow' so that ALL fields pass through without rejection. Real validation is done by validate_game_state()"

## Connections
- [[GameStateSchemaFieldConstants]] — related auto-generated constants
- [[EntitySchemaModelsPydantic]] — Pydantic-based entity tracking

## Contradictions
- None identified

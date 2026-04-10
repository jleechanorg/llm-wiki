---
title: "Schema Validation"
type: concept
tags: [validation, schema, type-safety, runtime]
sources: [gamestate-typeddict-schema-definitions]
last_updated: 2026-04-08
---

## Definition
Process of validating data structures against a defined schema to ensure they conform to expected shapes, types, and constraints.

## WorldAI Implementation
- **TypedDict Schema**: Auto-generated from game_state.schema.json
- **Runtime Validation**: GameState.to_validated_dict() enforces schema on every turn
- **Graceful Handling**: Handles invalid data gracefully without crashing

## Key Components
- **Schema Source**: game_state.schema.json defines canonical structure
- **Validation Layer**: Validates against schema before Firestore persistence
- **Error Handling**: Logs warnings without blocking on non-critical violations


## Related Concepts
- [[TypedDict]] — type definition mechanism
- [[TypeGuards]] — runtime type checking
- [[PydanticValidation]] — alternative validation approach

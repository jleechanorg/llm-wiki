---
title: "Schema Doc Caching"
type: concept
tags: [caching, performance, schema]
sources: []
last_updated: 2026-04-08
---

## Definition
Caching mechanism that pre-generates schema documentation at startup for fast retrieval during prompt injection. Eliminates repeated doc generation overhead on every prompt load.

## Key Properties
- **Per-type cache**: Individual cache entries per schema type (CombatState, CombatantState, etc.)
- **Timing targets**: <50ms generation per type, <500ms total initialization
- **Retrieval performance**: <1ms cache hits via get_cached_schema_doc()
- **Cold start**: Simulated via cache clear before initialization measurement

## Usage in System
Used by _inject_dynamic_schema_docs() to replace {{SCHEMA:TypeName}} placeholders with cached documentation.

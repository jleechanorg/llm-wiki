---
title: "Traceability Fields"
type: concept
tags: [data-architecture, firestore, debugging]
sources: ["structured-gemini-response-field-extraction"]
last_updated: 2026-04-08
---

Data architecture pattern storing full_state_updates and core_memories_snapshot alongside filtered LW subset, enabling downstream consumers to reconstruct full context without reading game_states/current_state.

## Connections
- [[Structured Gemini Response Field Extraction]] — implements traceability
- [[Sariel campaign replay desync measurement]] — uses for debugging

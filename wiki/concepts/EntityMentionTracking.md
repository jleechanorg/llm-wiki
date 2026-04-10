---
title: "Entity Mention Tracking"
type: concept
tags: [nlp, entity-extraction, llm, game-state]
sources: []
last_updated: 2026-04-08
---

## Definition
Entity mention tracking is the process of extracting and cataloging all named entities (characters, objects, locations) referenced in an LLM narrative response.

## Implementation
- LLM includes `entities_mentioned` array in structured JSON response
- Frontend renders as unordered list with 👥 emoji
- Enables downstream systems to track what entities are active in current scene

## Related Concepts
- [[Structured Fields]] — the schema field for entity mentions
- [[Entity Name Sanitization]] — safe ID generation for tracked entities

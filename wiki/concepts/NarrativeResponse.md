---
title: "NarrativeResponse"
type: concept
tags: [data-model, narrative, schema, pydantic]
sources: []
last_updated: 2026-04-08
---

## Definition
Pydantic model representing the structured response from the narrative engine. Includes narrative text, social_hp_challenge, and other game state updates.

## Key Fields
- `narrative`: Main text response
- `social_hp_challenge`: Optional dict with social encounter state
- `request_severity`: Normalized severity level (submission, information, etc.)
- `resistance_shown`: NPC resistance description

## Related Models
- [[Game State]]
- [[Schema Validation]]

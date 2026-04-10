---
title: "Firestore Document Trimming"
type: concept
tags: [firestore, optimization, data-management]
sources: ["structured-gemini-response-field-extraction"]
last_updated: 2026-04-08
---

Pattern for reducing large Firestore document size by: (1) summarizing large dict fields (item_registry, npc_data) with key counts, (2) trimming combat/encounter state to essential fields, (3) filtering player_character_data to core fields, (4) excluding story_history to stay under 1MB limit.

## Connections
- [[Structured Gemini Response Field Extraction]] — implements trimming pattern
- [[Real Service Provider Implementation]] — writes to Firestore

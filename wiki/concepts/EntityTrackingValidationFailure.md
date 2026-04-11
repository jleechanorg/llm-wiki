---
title: "Entity Tracking Validation Failure"
type: concept
tags: [entity-tracking, validation, narrative, llm, context-management]
sources: []
last_updated: 2026-04-11
---

## Description
Entity tracking validation consistently fails because entities mentioned in the narrative are not found in the `entity_tracking` context layer. The LLM generates narrative that names NPCs, locations, or objects that have been evicted from `entity_tracking` due to aggressive LRU tiering.

## Symptoms
- Entity validation passes 0-4% of the time
- Narrative mentions NPCs that are not in entity_tracking
- LRU tiering marks NPCs as 'dormant' too aggressively
- `ENTITY_TIERS: active=3/5, present=0` — no present-tier entities despite narrative need

## Root Cause
The LRU entity tiering system (introduced in ff79c3c4d, Dec 2025) aggressively evicts NPCs from active/present tiers when context pressure increases. The narrative generation layer is unaware of eviction — it generates mentions based on story logic, not tracking availability.

## Evidence
```
ENTITY_TRACKING_VALIDATION: Narrative failed entity validation
# Only 3 active entities, 0 present entities
# Narrative references evicted entities
```

## Fix
1. Lower eviction threshold so narrative-relevant NPCs stay in active tier
2. Add validation before narrative generation to ensure referenced entities are tracked
3. Distinguish between "present" (mentioned this turn) and "active" (needed for next turn)

## Connections
- [[Context-Bloat]] — root cause: entity tracking competes with other context
- [[LLMDrift]] — related: LLM losing track of state over time

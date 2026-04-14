---
title: "mvp_site entities_pydantic"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/entities_pydantic.py
---

## Summary
Pydantic schema models for entity tracking using sequence ID format. Provides EntityType enum (PLAYER_CHARACTER, NPC, CREATURE, LOCATION, ITEM, FACTION), CombatDisposition enum for allegiance classification, and sanitize_entity_name_for_id() for entity ID generation.

## Key Claims
- EntityType enum: PLAYER_CHARACTER, NPC, CREATURE, LOCATION, ITEM, FACTION, OBJECT
- CombatDisposition enum: FRIENDLY (PC/companions preserved), HOSTILE (enemies removed on defeat), NEUTRAL (bystanders)
- sanitize_entity_name_for_id() converts entity names to valid ID format (lowercase, underscores)
- Uses DefensiveNumericConverter for robust numeric field handling

## Connections
- [[EntityTracking]] — Pydantic models for entity schema validation
- [[CombatSystem]] — combat disposition classification

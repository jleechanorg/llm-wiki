---
title: "Structured Gemini Response Field Extraction"
type: source
tags: [python, gemini, extraction, firestore, state-management]
source_file: "raw/structured-gemini-response-field-extraction.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python utility module providing helpers for extracting structured Gemini response fields with type safety, default handling, and Firestore document size management. Includes functions for trimming large state updates and building traceability fields.

## Key Claims
- **_get_structured_attr**: Returns structured response attribute with typed default, handles None/falsy values via optional `treat_falsy_as_default` flag
- **_summarize_mapping**: Summarizes dict by counting keys and providing sample keys for debugging
- **_audit_trim_state_update**: Trims large state_update values (item_registry, npc_data, combat_state, encounter_state, player_character_data) to reduce Firestore document size risk
- **_trim_custom_campaign_state**: Excludes known-large fields (story_history) from custom_campaign_state
- **_build_traceability_fields**: Builds full_state_updates + core_memories_snapshot for per-entry traceability without exceeding 1MB Firestore limit
- **_build_state_updates_audit_subset**: Creates audit subset of specific state keys for compliance tracking
- **_normalize_resources_for_story_entry**: Normalizes resources to StoryEntry contract string type (JSON serialization for dict/list)

## Key Quotes
> "We coerce ``None`` back to the supplied ``default`` so callers always receive the expected type (``str``/``list``/``dict``)." — on default handling

> "story_history is excluded from full_state_updates to stay under the Firestore 1 MB document limit." — on traceability fields

## Connections
- [[StreamEvent SSE type for streaming]] — related streaming response handling
- [[Sariel campaign replay desync measurement]] — entity tracking state issues
- [[Real Service Provider Implementation]] — Firestore integration patterns

## Contradictions
- None identified

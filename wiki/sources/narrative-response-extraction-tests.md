---
title: "Narrative Response Extraction Tests"
type: source
tags: [python, testing, structured-fields, llm-response]
source_file: "raw/test_narrative_response_extraction.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests for NarrativeResponse extraction from LLMResponse. Tests the mapping and validation of structured fields including session_header, planning_block, dice_rolls, resources, debug_info, entities_mentioned, and location_confirmed.

## Key Claims
- **Full NarrativeResponse initialization**: All structured fields can be set including narrative, session_header, planning_block, dice_rolls, resources, debug_info, entities_mentioned, and location_confirmed
- **Planning block choice extraction**: The _choices_by_id helper function converts planning block choices from dict or list format to a normalized dict by choice ID
- **Default values**: Minimal initialization with just narrative sets appropriate defaults for optional fields
- **None value handling**: NarrativeResponse should handle None values for optional fields gracefully

## Key Quotes
> "The _choices_by_id helper extracts choices from planning_block and normalizes them to a dict keyed by choice_id"

## Connections
- [[Narrative Response Schema]] — the module being tested for structured field handling
- [[LLM Response Object TDD Tests]] — related tests for LLMResponse class

## Contradictions
- None identified

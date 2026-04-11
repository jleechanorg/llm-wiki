---
title: "LLMResponse Object TDD Tests"
type: source
tags: [python, testing, tdd, llm-response, debug-tags]
source_file: "raw/test_llm_response_object_tdd.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test-driven development tests for LLMResponse object, defining expected behavior for cleaning up architecture between llm_service and main.py. Tests cover LLMResponse.create() parsing of raw response text, debug tags detection, state updates extraction, and entities mentioned.

## Key Claims
- **LLMResponse.create()**: Takes raw response text and parses structured fields including narrative, debug_info, state_updates, entities_mentioned, and location_confirmed
- **Debug tags detection**: Automatically detects dm_notes, dice_rolls, resources, and state_rationale from debug_info block
- **has_debug_content**: Boolean property indicating whether any debug tags contain actual content
- **state_updates property**: Returns state_updates from structured response for game state updates
- **entities_mentioned property**: Returns list of entities extracted from the response

## Test Coverage
- test_gemini_response_creation: Validates basic LLMResponse object creation with core fields
- test_debug_tags_detection_with_content: Verifies debug tags detected when content exists
- test_debug_tags_detection_no_content: Verifies empty debug tags handled correctly
- test_state_updates_property: Validates state_updates extraction
- test_entities_mentioned_property: Validates entities_mentioned extraction

## Connections
- [[LLMResponse]] — main class under test
- [[LLMResponse.create]] — method being validated
- [[parse_structured_response]] — helper function for JSON parsing
- [[NarrativeResponse]] — schema class for structured response parsing
- [[Debug Tags Detection]] — concept of extracting debug metadata from LLM responses

## Contradictions
- None identified

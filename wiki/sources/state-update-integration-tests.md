---
title: "State Update Integration Tests"
type: source
tags: [integration, testing, json, state-management, python, flask]
source_file: "raw/state-update-integration-tests.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Integration tests for state update flow in the JSON response system. This test suite specifically targets Bug 1: LLM Not Respecting Character Actions by testing the complete flow from AI response to state application.

## Key Claims
- **State Updates Extracted from JSON**: The `parse_structured_response` function correctly extracts `state_updates` from JSON responses, separating them from narrative text
- **State Updates Don't Leak into Narrative**: Verified that state update keys (`state_updates`, `player_character_data`, `hp_current`, `combat_round`) don't appear in the narrative output
- **Valid State Update Values**: Tests verify specific state update values like `hp_current: "20"` for player and `hp_current: "5"`, `status: "wounded"` for NPCs are properly handled
- **JSON Mode vs Markdown Blocks**: System correctly prioritizes JSON-based state_updates over markdown [STATE_UPDATES_PROPOSED] blocks

## Test Coverage
- `test_state_updates_extracted_from_json_response`: Verifies state updates accessible through LLMResponse.state_updates property
- `test_main_py_uses_json_state_updates_not_markdown_blocks`: Validates main.py correctly uses structured_response.state_updates
- `test_no_state_updates_proposed_blocks_in_json_mode`: Ensures JSON state updates take precedence over markdown blocks
- `test_empty_narrative_with_state_updates_only`: Tests handling of responses with only state updates

## Connections
- [[StateUpdateFlow]] — the overall flow from AI response to game state
- [[LLMResponse]] — class that wraps narrative and structured response
- [[NarrativeResponse]] — schema for structured LLM responses with state_updates

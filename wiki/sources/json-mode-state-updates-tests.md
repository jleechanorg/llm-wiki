---
title: "JSON Mode State Updates Tests"
type: source
tags: [python, testing, json-mode, state-updates, llm-response]
source_file: "raw/test_json_mode_state_updates.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite verifying that state updates are properly extracted from JSON responses in LLMResponse. Tests confirm that narrative text excludes state update blocks, and that structured responses contain the parsed state updates.

## Key Claims
- **State updates extracted from JSON**: When JSON response contains state_updates field, they are available in structured_response.state_updates
- **Narrative excludes state data**: Parsed narrative text does not contain [STATE_UPDATES_PROPOSED] blocks or raw JSON keys
- **Empty state updates handled**: Responses with empty state_updates dict don't trigger STATE_UPDATES_PROPOSED blocks
- **No state updates = clean narrative**: Responses without state_updates field work correctly without adding blocks

## Key Quotes
> "Check that state updates are NOT in the narrative text (bug fix)" — validates fix for state data leaking into story text

## Connections
- [[LLMResponse]] — class under test
- [[JSON Mode]] — response parsing mode being validated
- [[State Updates]] — structured data mechanism for game state changes
- [[GOD MODE]] — related mode that also uses structured JSON responses

## Contradictions
- None detected

---
title: "God Mode Response Field Tests"
type: source
tags: [python, testing, god-mode, response-field, schema]
source_file: "raw/test_god_mode_response_field.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite validating that god mode responses use the god_mode_response field correctly. Tests verify the parsing and handling of god_mode_response in structured JSON responses, distinguishing it from standard narrative responses.

## Key Claims
- **Frontend field separation**: god_mode_response is a separate field from narrative, used directly by frontend for god mode responses
- **Empty narrative behavior**: When god_mode_response is present, narrative should be empty string
- **Normal response compatibility**: Non-god mode responses use narrative field as before
- **State updates support**: god_mode_response responses can include complex state_updates including npc_data, environment, etc.
- **Malformed JSON handling**: Returns standard error message on parse failure

## Key Quotes
> "Narrative should be empty - frontend uses god_mode_response directly" — Test assertion comment

## Connections
- [[God Mode Planning Blocks Tests]] — Related god mode test suite
- [[God Mode Narrative Validation Placeholder Tests]] — Related god mode validation
- [[parse_structured_response]] — Function being tested

## Contradictions
- None

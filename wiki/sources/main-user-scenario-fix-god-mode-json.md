---
title: "Main User Scenario Fix — No Raw JSON in God Mode"
type: source
tags: [testing, god-mode, json-parsing, tdd, mvp-site]
source_file: "raw/main_user_scenario_fix_test.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests validating the main user scenario fix — no more raw JSON displayed in god mode. Tests verify that malformed JSON responses from the AI are caught and converted to standardized error messages instead of exposing raw JSON keys like `god_mode_response` and `state_updates` to users.

## Key Claims
- **Primary Fix**: Malformed JSON no longer leaks raw JSON keys to users in god mode
- **Error Standardization**: Invalid JSON returns standardized "invalid json response" message
- **Content Readability**: User sees readable error text, not JSON structure
- **Normal Operations**: Valid god mode responses continue to work correctly
- **Edge Cases**: Tests cover missing braces, invalid JSON syntax, and truncated responses

## Test Coverage
- `test_luke_scenario_scene_116_type_issue`: Exact scenario that caused Luke's issue with malformed god mode JSON
- `test_various_malformation_scenarios`: Tests multiple malformation types (missing brace, invalid syntax, truncated)
- `test_normal_god_mode_still_works`: Ensures valid god mode responses continue functioning

## Key Quotes
> "User should never see raw JSON keys" — test assertion for god_mode_response
> "User should never see raw JSON keys" — test assertion for narrative

## Connections
- [[ParseStructuredResponse]] — function that parses AI responses and handles errors
- [[GodMode]] — game mode where AI responds without advancing narrative
- [[NarrativeResponseSchema]] — schema defining expected AI response format

## Contradictions
- None identified

---
title: "parse_structured_response"
type: entity
tags: [function, json, parsing]
sources: [safer-json-cleanup-tests]
last_updated: 2026-04-08
---

## Summary
Function that parses JSON-structured responses from LLM output. Extracts narrative text, entities_mentioned, and location_confirmed from JSON-formatted strings. Returns error narrative when JSON is invalid.

## Behavior
- Parses valid JSON: extracts fields (narrative, entities_mentioned, location_confirmed)
- Handles malformed JSON: returns error message (recovery disabled per tests)
- Preserves JSON-like text in narrative: brackets, quotes, braces kept intact

## Test Coverage
- Safe JSON Cleanup Tests: narrative with JSON-like content preserved
- Field Format Validation: story vs text field format handling

---
title: "Gemini Response Validation Tests"
type: source
tags: [python, testing, json, parsing, validation, gemini]
source_file: "raw/test_gemini_response_validation.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite validating Gemini API response validation and parsing in llm_service.py. Focuses on JSON parsing, schema validation, field validation, and handling of malformed/truncated responses. Tests validate that the system returns error responses for invalid JSON rather than attempting recovery (per PR #3458).

## Key Claims
- **Valid JSON parsing**: parse_structured_response() correctly parses JSON responses into NarrativeResponse objects
- **Markdown-wrapped JSON**: System extracts JSON from markdown code blocks (```json ... ```)
- **Invalid JSON error handling**: Malformed JSON returns error response without recovery (per PR #3458)
- **Truncated JSON error handling**: Truncated JSON returns error response without partial recovery (per PR #3458)
- **Extra data recovery**: Valid JSON followed by extra text IS recovered successfully
- **dice_audit_events parsing**: Parses as list[dict], ignoring invalid items gracefully

## Key Quotes
> "Test that valid JSON responses are parsed correctly." — test_valid_json_parsing
> "Test that malformed JSON returns error response (no recovery per PR #3458)." — test_invalid_json_returns_error_response

## Connections
- [[NarrativeResponse]] — Pydantic schema for structured responses
- [[ParseStructuredResponse]] — function that extracts and parses JSON from LLM output
- [[PR3458]] — PR that removed JSON recovery for malformed/truncated responses

## Contradictions
- None identified

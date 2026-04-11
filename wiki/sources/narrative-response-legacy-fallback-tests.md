---
title: "Narrative Response Legacy JSON Cleanup Tests"
type: source
tags: [python, testing, json, error-handling, regression, narrative-response]
source_file: "raw/test_narrative_response_legacy_fallback.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test coverage for legacy JSON cleanup code in narrative_response_schema.py (lines 500-557). Tests various malformed JSON scenarios including aggressive cleanup, JSON artifact removal, nested string escapes, and fallback behavior when JSON parsing fails.

## Key Claims
- **Malformed JSON aggressive cleanup**: Severely broken JSON with missing braces triggers error recovery path
- **JSON artifact cleanup**: Text with embedded JSON markers like `"narrative":` gets cleaned up
- **Nested JSON string escapes**: Handles escaped quotes and newlines within narrative content
- **Fallback without narrative field**: JSON without a narrative field applies minimal cleanup and returns content
- **Multiple narrative patterns**: Multiple `"narrative":` markers in text trigger error path
- **Whitespace normalization**: Excessive spaces and newlines in narrative content are handled

## Key Quotes
> "Should return error message as recovery is disabled" — Tests verify that recovery is now disabled

## Connections
- [[NarrativeResponse Extraction Tests]] — Related test file for NarrativeResponse parsing
- [[Narrative Response Error Handling Tests]] — Error handling and type conversion tests
- [[LLMResponse Structured Fields Parsing]] — Structured field parsing from raw JSON

## Contradictions
- None identified

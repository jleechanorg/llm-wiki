---
title: "TDD Tests for _classify_raw_narrative Helper"
type: source
tags: [python, testing, tdd, narrative-classification, llm-service]
source_file: "raw/test_classify_raw_narrative.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit test suite defining the contract for `_classify_raw_narrative(text) -> bool` helper in `mvp_site.llm_service`. The helper determines whether text should be used as streaming fallback for narrative generation. Returns True for genuine narrative strings (prose, quoted JSON strings) and False for empty, marker, JSON containers, and malformed JSON.

## Key Claims
- **Plain Prose**: Simple prose like "You wait in silence." returns True and should be used as fallback
- **Short Narratives**: Short narratives (≤20 chars) must NOT be rejected — "You wait." returns True
- **JSON Quoted Strings**: `json.loads('"You wait."')` returns str — must be treated as valid narrative
- **Empty/Whitespace**: Empty strings and whitespace-only text return False
- **Marker Detection**: `JSON_PARSE_FALLBACK_MARKER` returns False and must not be used as narrative
- **JSON Containers**: JSON objects `{}` and arrays `[]` return False — not narrative content
- **JSON Scalars**: null, true, false, numbers return False — not narrative
- **No Alpha Chars**: Text with no alphabetic characters (e.g., "12345 !@#$%") returns False
- **Malformed JSON Protection**: Malformed JSON starting with `{` or `[` must return False to prevent raw JSON being stored as story text

## Connections
- [[JSONParseFallbackMarker]] — constant that marks fallback responses, must be excluded from narrative classification
- [[LLMServiceModule]] — module containing the `_classify_raw_narrative` helper

## Contradictions
- None identified

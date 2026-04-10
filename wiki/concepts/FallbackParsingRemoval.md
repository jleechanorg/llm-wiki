---
title: "Fallback Parsing Removal"
type: concept
tags: [legacy-code, refactoring, testing]
sources: ["json-only-comprehensive-tests"]
last_updated: 2026-04-08
---

## Definition
Fallback Parsing Removal refers to the elimination of legacy regex-based extraction of state updates from markdown-style [STATE_UPDATES_PROPOSED] blocks in LLM narrative text. This was replaced by exclusive JSON-based state delivery.

## Removed Functions
- parse_llm_response_for_state_changes — no longer exists
- _clean_markdown_from_json — helper also removed

## Migration Path
1. All state updates now come from structured JSON responses
2. generate_json_mode_content enforces JSON output format
3. LLMResponse.state_updates reads directly from JSON field
4. No attempt to parse narrative text for state data

## Test Validation
- test_parse_llm_response_for_state_changes_should_not_exist verifies removal
- test_no_regex_state_update_extraction confirms no extraction from markdown
- test_always_structured_response_required validates empty state_updates when no JSON

## Related Concepts
- [[JSON Mode]] — the replacement for fallback parsing
- [[Structured Response]] — current source of state updates
- [[Regex Extraction]] — the removed legacy approach
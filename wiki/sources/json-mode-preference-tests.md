---
title: "JSON Mode Preference Tests"
type: source
tags: [python, testing, json-mode, state-updates, parsing]
source_file: "raw/test_json_mode_preference.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite verifying that JSON mode is always preferred over regex/markdown parsing when available. Tests confirm that structured JSON responses take precedence over [STATE_UPDATES_PROPOSED] markdown blocks, and that no fallback parsing mechanism exists.

## Key Claims
- **JSON preferred over markdown**: When both JSON and [STATE_UPDATES_PROPOSED] blocks exist, JSON values are used
- **No fallback parsing**: parse_llm_response_for_state_changes function no longer exists
- **No state without JSON**: Empty state updates when no structured JSON response is provided
- **Debug stripping safe**: strip_debug_content does not interfere with JSON state updates
- **Code block extraction**: JSON can be extracted from both ```json and generic ``` code blocks

## Key Quotes
> "When both JSON and markdown blocks exist, JSON is used"

> "JSON mode is the ONLY mode - no fallback"

## Connections
- [[JSON Mode]] — core preference system being tested
- [[State Updates]] — structured updates extracted from JSON responses
- [[Code Block Parsing]] — JSON extraction from markdown code blocks

## Contradictions
- None identified

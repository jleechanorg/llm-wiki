---
title: "mvp_site narrative_response_schema"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/narrative_response_schema.py
---

## Summary
Simplified structured narrative generation schemas for parsing LLM JSON responses. Provides parse_structured_response() with markdown code block extraction, JSON recovery from "Extra data" errors, and MIN_NARRATIVE_LENGTH = 100 for suspicious shortness detection.

## Key Claims
- JSON_MARKDOWN_PATTERN extracts JSON from ```json code blocks
- JSON_PARSE_FALLBACK_MARKER = "Invalid JSON response received" for parse failure detection
- _log_thresholded_warning() per-process warning escalation: INFO until threshold, then WARNING/ERROR
- MIN_NARRATIVE_LENGTH = 100 for "suspiciously short" narrative detection
- Uses json_utils.find_matching_brace and extract_best_json

## Connections
- [[LLMIntegration]] — structured response parsing
- [[Validation]] — narrative shortness validation

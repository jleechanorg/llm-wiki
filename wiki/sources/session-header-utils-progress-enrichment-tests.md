---
title: "Session Header Utils Progress Enrichment Tests"
type: source
tags: [unit-testing, session-headers, progress-enrichment, python, tdd]
source_file: "raw/session-header-utils-progress-enrichment-tests.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests for session header progress enrichment functionality in `world_logic.py`. Tests cover XP/gold display formatting, session header normalization, and dictionary-format conversion.

## Key Claims
- **_enrich_session_header_with_progress**: Enriches empty headers with XP/gold progress data, appends to existing status lines, respects existing tokens
- **Dict Format Normalization**: Converts JSON dict format to proper string format with [SESSION_HEADER] prefix
- **Prefix Handling**: Adds missing [SESSION_HEADER] prefix when absent
- **Edge Cases**: Handles zero next_level, missing progress data gracefully

## Key Test Functions
- `test_enriches_empty_header_with_progress`: Validates XP: 120/200 | Gold: 50gp formatting
- `test_enriches_status_line`: Validates appending to existing Status line
- `test_appends_to_last_line_without_status`: Appends to last line when no Status field
- `test_respects_existing_tokens`: Skips enrichment when tokens already present
- `test_handles_zero_next_level`: Handles zero denominator in XP ratio
- `test_skips_missing_progress_data`: Gracefully handles empty character data
- `test_normalizes_dict_format_session_header`: Converts JSON dict to proper session header string
- `test_adds_missing_session_header_prefix`: Adds [SESSION_HEADER] prefix when missing

## Connections
- [[session-header-utils-edge-cases-pr3746]] — related edge case tests for session headers

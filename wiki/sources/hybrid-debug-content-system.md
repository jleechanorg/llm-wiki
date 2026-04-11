---
title: "Hybrid Debug Content System for Backward Compatibility"
type: source
tags: [python, debug, backward-compatibility, json-parsing]
source_file: "raw/hybrid-debug-content-system.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module providing backward compatibility functions for handling debug content in both old campaigns with embedded debug tags (e.g., `[DEBUG_START]`) and new campaigns with structured `debug_info` fields. Includes bracket-aware JSON extraction, comprehensive Unicode escape handling, and debug content stripping.

## Key Claims
- **Bracket-aware JSON Extraction**: `_extract_nested_object()` correctly handles nested braces by counting open/close braces while respecting string boundaries, unlike simple regex that truncates on first closing brace
- **Unicode Escape Handling**: `_unescape_json_string()` handles standard JSON escapes (\n, \t, \r, etc.), unicode escapes (\uXXXX), and surrogate pairs for characters outside the Basic Multilingual Plane
- **Multiple Debug Pattern Types**: Supports old-style `[DEBUG_START]` / `[DEBUG_END]` tags, Markdown-formatted debug blocks, and inline JSON `debug_info` objects
- **Backward Compatibility Layer**: Enables migration from embedded debug tags to structured debug_info fields without breaking existing campaign data

## Key Quotes
> "This handles nested braces correctly, unlike simple regex patterns that truncate on the first closing brace." — explaining the bracket-aware parsing approach

> "Handle surrogate pairs when present." — unicode handling for non-BMP characters

## Connections
- [[llm_response]] — shares DEBUG_START_PATTERN and DEBUG_STATE_PATTERN with this module
- [[narrative_response_schema]] — shares JSON cleanup patterns (NARRATIVE_PATTERN, JSON_STRUCTURE_PATTERN)
- [[mvp_site]] — the parent module this code belongs to

## Contradictions
- None identified — this module is complementary to existing debug handling in llm_response.py and narrative_response_schema.py

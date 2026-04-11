---
title: "Debug Content Stripping Tests"
type: source
tags: [python, testing, json, text-processing, debug]
source_file: "raw/test_debug_content_strip.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests validating debug_info removal from JSON strings within narrative text. Tests verify that the hybrid system can detect and strip embedded debug metadata while preserving surrounding content.

## Key Claims
- **Inline Debug Detection**: Identifies debug_info keys nested within JSON objects in plain text
- **Whitespace Handling**: Strips debug content regardless of spacing around colons and braces
- **Preservation**: Maintains surrounding text outside the debug block intact

## Key Quotes
> "Before {\"narrative\":\"hi\",\"debug_info\":{\"nested\":{\"k\":\"v\"}}\",\"x\":1} After"

## Connections
- [[DebugHybridSystem]] — the module being tested
- [[JSONParsing]] — debug_info detection relies on JSON structure recognition

## Contradictions
- None

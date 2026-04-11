---
title: "Gemini Native Tools Tests"
type: source
tags: [python, testing, gemini, native-tools, function-calling]
source_file: "raw/test_gemini_native_tools.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests validating the Gemini native-tools path in mvp_site.llm_providers.gemini_provider module. Tests verify that native tools mode does not force tool calling and handles edge cases like mismatched tool results.

## Key Claims
- **No forced tool calling**: Gemini native-tools path uses mode='AUTO' rather than 'ANY', avoiding forced function calls when the model produces narrative-only responses
- **Fallback to JSON mode**: No-roll turns still produce valid JSON responses via Phase 2 fallback to generate_json_mode_content
- **Tool result mismatch handling**: Logs warning when len(tool_results) != len(tool_requests)

## Connections
- [[GeminiProvider]] — module under test
- [[FunctionCallingMode]] — AUTO vs ANY mode distinction
- [[Phase1Phase2Fallback]] — narrative-to-JSON fallback pattern

## Contradictions
- None identified

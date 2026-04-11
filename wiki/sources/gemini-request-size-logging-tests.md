---
title: "Gemini Request Size Logging Tests"
type: source
tags: [python, testing, logging, gemini, request-metrics]
source_file: "raw/test_gemini_request_size_logging.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests validating request size logging in `generate_json_mode_content`. Tests verify that request size metrics (characters, tokens, bytes) are correctly logged before API calls, including defensive handling for various content structures (Content objects with parts, string lists, and single strings).

## Key Claims
- **Content metrics logging**: Request size is logged with breakdown for contents, system instruction, and total (in characters/tokens/bytes format)
- **Multiple content formats**: Tests handle Content objects with parts, list of strings, and single string content types
- **Defensive handling**: Tests verify logging works even with different content structure types
- **Mock verification**: Uses mocks to verify GEMINI_REQUEST log messages contain expected metric fields

## Key Quotes
> "contents=...ch/...tk/...b, system=...ch/...tk/...b, total=...ch/...tk/...b, model=..." — log format pattern

## Connections
- [[GeminiProvider]] — module under test
- [[GenerateJsonModeContent]] — function being tested
- [[LLMRequest]] — request type used in logging
- [[RequestSizeMetrics]] — metrics being logged (characters, tokens, bytes)

## Contradictions
- []

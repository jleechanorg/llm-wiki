---
title: "LLMRequest Class TDD Tests"
type: source
tags: [python, testing, tdd, llm, gemini, json]
source_file: "raw/test_llm_request_class_tdd.py"
sources: []
last_updated: 2026-04-08
---

## Summary
TDD test suite validating that the LLMRequest class sends structured JSON directly to Gemini API instead of converting JSON back to concatenated string blobs. Tests follow RED→GREEN→REFACTOR approach where initial tests FAIL until LLMRequest class is properly implemented.

## Key Claims
- **Structured JSON requirement**: Gemini API should receive structured JSON string, not concatenated string blobs via to_gemini_format()
- **continue_story integration**: continue_story() should pass structured JSON through to Gemini API calls
- **Test mode bypass**: TESTING_AUTH_BYPASS environment variable enables test execution without API keys

## Key Quotes
> "The content sent to Gemini should be structured JSON string, not concatenated blob"

## Connections
- [[Gemini API]] — target API for structured JSON submission
- [[Test-Driven Development]] — methodology used for LLMRequest implementation
- [[GameState]] — provides game state data for story generation

## Contradictions
- None identified

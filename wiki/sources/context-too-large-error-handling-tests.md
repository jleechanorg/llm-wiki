---
title: "ContextTooLargeError Handling Tests"
type: source
tags: [python, testing, error-handling, http-status, context-compaction, llm-providers]
source_file: "raw/test_context_too_large_error_handling.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite validating that ContextTooLargeError from LLM providers is properly handled. Tests verify the error is caught and converted to LLMRequestError with HTTP 422 status (Unprocessable Entity), providing clear user feedback instead of generic 500 errors. Also tests provider fallback behavior when API keys are missing.

## Key Claims
- **422 Status Code**: ContextTooLargeError converts to LLMRequestError with 422 status for clear HTTP feedback
- **Helpful Messages**: Error messages contain useful debugging information like token counts
- **Provider Fallback**: System gracefully falls back to alternate providers (e.g., Cerebras) when default provider's API key is missing
- **Dual Routing**: Tests cover both native tools and JSON-first tool_requests code paths

## Key Quotes
> "Context too large: prompt used 100,000 tokens" — example error message with token metadata

## Connections
- [[Context Budgeting and Allocation TDD Tests]] — related to context size management
- [[Cerebras json_schema strict:false TDD Tests]] — Cerebras provider testing

## Contradictions
- None identified

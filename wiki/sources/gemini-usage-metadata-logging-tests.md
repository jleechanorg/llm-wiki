---
title: "Gemini Usage Metadata Logging Tests"
type: source
tags: [python, testing, logging, gemini, caching, usage-metrics]
source_file: "raw/test_gemini_usage_metadata_logging.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test coverage for Gemini usage_metadata logging in _call_llm_api. Ensures that usage metadata is correctly logged for implicit caching verification, including defensive null handling for None values and missing attributes.

## Key Claims
- **Cache hit rate calculation**: When cached_content_token_count=172648 and prompt_token_count=230197, cache_hit_rate=75.0%
- **Defensive null handling**: Tests verify logging works when usage_metadata fields are None
- **Missing attribute handling**: Tests handle AttributeError when cached_content_token_count doesn't exist
- **Multiple provider paths**: Tests cover both native_tools and code_execution code paths

## Key Quotes
> "Ensures that usage metadata is correctly logged for implicit caching verification"

## Connections
- [[GeminiAPI]] — provider being tested
- [[LLMService]] — service containing _call_llm_api function
- [[ImplicitCaching]] — feature being verified through usage metadata

## Contradictions
- None identified

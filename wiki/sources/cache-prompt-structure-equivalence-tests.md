---
title: "Cache Prompt Structure Equivalence Tests"
type: source
tags: [python, testing, unittest, cache, prefix-caching, equivalence-validation]
source_file: "raw/cache-prompt-structure-equivalence-tests.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest validating that LLMRequest.to_explicit_cache_parts() correctly splits content into cacheable and uncacheable parts while preserving byte-for-byte equivalence with the implicit (single-JSON-blob) caching approach. Critical for prefix-based caching where field ordering matters.

## Key Claims
- **Field Ordering Preserved**: Implicit and explicit approaches maintain identical key ordering (critical for prefix-based caching)
- **JSON Payload Equivalence**: Merged explicit parts equal implicit JSON byte-for-byte
- **Correct Cache Split**: First 15 story_history entries are cacheable, remaining 5 are uncacheable
- **Structure Merging**: story_history arrays are concatenated, other fields merged correctly

## Key Quotes
> "CRITICAL: Validate field ordering (prefix-based caching depends on this!)"

> "CRITICAL: Validate actual JSON payloads (what gets sent to Gemini!)"

## Connections
- [[LLMRequest]] — class being tested
- [[PrefixBasedCaching]] — the caching strategy this test validates
- [[CachePromptStructure]] — the structure being validated

## Contradictions
- None identified

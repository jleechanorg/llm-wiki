---
title: "TDD Tests for Cache + Provably Fair Compatibility"
type: source
tags: [python, testing, unittest, tdd, cache, provably-fair, gemini, seed-injection]
source_file: "raw/tdd-tests-cache-provably-fair-compatibility.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest suite validating cache compatibility with provably fair seed injection in the Gemini provider. Tests verify that cache_name flows through to API calls, provably fair seed is injected as a content part (not in system_instruction), and native tools path does not disable caching. Layer 1 unit test — no server required.

## Key Claims
- **cache_name Flow-Through**: generate_content_with_code_execution must pass cache_name to API, not None
- **Seed Injected as Content Part**: Provably fair seed must appear in prompt_contents, not system_instruction
- **System Instruction Omitted**: When using cached_content, system_instruction is omitted from request payload
- **Seed Override Contains Hex**: First content part must contain PROVABLY_FAIR_SEED_OVERRIDE with actual hex seed
- **Native Tools Preserves Cache**: Native-tools cache path keeps cache active and suppresses phase1 system_instruction

## Key Quotes
> "cache_name must flow through to generate_json_mode_content, not be set to None"

> "seed part should be prepended"

> "system_instruction must be omitted when using cached_content"

## Connections
- [[CacheCaching]] — prefix-based caching requires field ordering consistency
- [[ProvablyFair]] — seed injection pattern for deterministic dice rolls
- [[GeminiProvider]] — Google Genai wrapper for LLM calls
- [[ContentParts]] — Gemini content structure for messages

## Contradictions
- None detected

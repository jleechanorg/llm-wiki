---
title: "test_cache_provably_fair.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
TDD tests for cache + provably fair compatibility. Verifies cache remains active when provably fair seed is injected.

## Key Claims
- `generate_content_with_code_execution` passes cache_name through to API (not None)
- Provably fair seed injected as content part, not in system_instruction
- system_instruction omitted when using cached_content
- `generate_content_with_native_tools` preserves cache_name even when tool_requests exist
- Phase1 system_instruction suppressed when cache_name is set

## Connections
- [[gemini_provider]] — the module being tested
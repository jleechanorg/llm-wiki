---
title: "PromptGenerator"
type: entity
tags: [python-module, prompt-engineering, code-centralization]
sources: []
last_updated: 2026-04-08
---

Python module that centralizes ALL prompt manipulation code for the application. Located in the mvp_site package, it handles system instruction loading, caching, continuation building, temporal correction, and current turn formatting.

## Purpose
Provides a single source of truth for prompt construction, allowing llm_service and world_logic to focus on request/response orchestration.

## Key Features
- PATH_MAP with 25+ prompt type definitions
- Schema documentation cache (_SCHEMA_DOC_CACHE)
- Feature flag support (ENABLE_PROMPT_COMMENT_STRIPPING)
- Runtime-checkable AgentProtocol
- TARGET_WORD_COUNT = 300 for story continuations

## Related
- [[llm-service]]
- [[world-logic]]
- [[SystemInstruction]]

---
title: "Prompt Building Utilities for Agent-Based System Instructions"
type: source
tags: [prompt-engineering, system-instructions, llm-service, world-logic, code-centralization]
source_file: "raw/prompt-building-utilities-agent-system-instructions.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module centralizing ALL prompt manipulation code for the application. Handles system instruction loading/caching, continuation prompt building, temporal correction prompts, static prompt parts generation, and current turn prompt formatting. Allows llm_service and world_logic to focus on request/response orchestration instead of prompt construction.

## Key Claims
- **Centralization**: Single source of truth for all prompt manipulation across llm_service.py and world_logic.py
- **System Instruction Loading**: Reads and caches prompt files from filesystem
- **Continuation Prompt Building**: Constructs prompts for ongoing story/narrative continuations
- **Temporal Correction**: Handles time-based prompt adjustments
- **Schema Documentation Cache**: Populated at module import time for schema documentation strings
- **Feature Flag Control**: ENABLE_PROMPT_COMMENT_STRIPPING controls comment stripping from prompt files

## Key Components
- PATH_MAP: Centralized mapping of prompt types to file paths (25+ prompt types)
- TARGET_WORD_COUNT: 300 words for standard story continuations
- AgentProtocol: Runtime-checkable protocol for agents
- Support for narrative, mechanics, dice, game state, character creation, combat, faction management, relationship, reputation, and more prompt types

## Connections
- [[llm-service]] — delegates prompt construction to this module
- [[world-logic]] — delegates prompt construction to this module
- [[SystemInstruction]] — core concept this module manages
- [[PromptEngineering]] — the discipline this code implements

## Contradictions
- None identified

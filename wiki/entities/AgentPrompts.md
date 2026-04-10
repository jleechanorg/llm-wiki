---
title: "AgentPrompts"
type: entity
tags: [module, prompt-loading]
sources: ["test-prompt-loading-via-service"]
last_updated: 2026-04-08
---

Python module responsible for loading prompt files from disk. Provides `_load_instruction_file` function and `PATH_MAP` constant that maps prompt types to file paths.

## Key Functions
- `_load_instruction_file(p_type)` — loads and returns prompt content for given type
- `_loaded_instructions_cache` — in-memory cache for loaded prompts

## Usage
Used by [[PromptBuilder]] to construct prompts for LLM calls.

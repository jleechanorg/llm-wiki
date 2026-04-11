---
title: "Prompt Variant Loading System"
type: source
tags: [prompt-engineering, dice-strategy, llm, system-instructions, versioning]
source_file: "raw/prompt_variant_loader.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module providing a prompt variant loading system for dice strategy-specific prompts. Replaces hidden string injection at runtime with explicit, version-controlled markdown prompt files that can be reviewed, tested, and version-controlled independently.

## Key Claims
- **Explicit Variant Loading** — Loads different prompt files based on dice strategy (code_execution, tool_requests, native, native_two_phase) instead of injecting override strings at runtime.
- **Version-Controlled Prompts** — All prompt variants are markdown files that can be reviewed, version-controlled, and tested independently.
- **Fallback Logic** — When code_execution variant is missing, gracefully falls back to the default prompt file.
- **Directory-Based Organization** — Stores prompt files in a `prompts/` subdirectory relative to the loader module.

## Key Quotes
> "This replaces the previous approach of injecting code_exec_override strings at runtime." — documents the motivation for the refactoring.

## Connections
- [[DiceStrategy]] — The parameter type driving variant selection
- [[SystemInstruction]] — The concept of system-level prompts in LLM interactions
- [[PromptEngineering]] — The broader practice this module implements

## Contradictions
- None identified yet. The source explicitly replaces a previous hidden injection approach, which may be documented elsewhere in the wiki.

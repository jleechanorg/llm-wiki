---
title: "Prompt Loading Service Tests"
type: source
tags: [python, testing, prompt-loading, agent-prompts, cache]
source_file: "raw/test_prompt_loading_via_service.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests validating prompt file loading through the agent_prompts service. Tests ensure all prompt files registered in PATH_MAP are loadable, unknown prompt types raise ValueError, all .md files in prompts/ are registered in the service, and all registered prompts are actually used in the codebase.

## Key Claims
- **Prompt loading via service**: Calling `_load_instruction_file(p_type)` loads prompt content from disk for registered prompt types.
- **Unknown prompt type raises error**: Calling `_load_instruction_file` with an unregistered type raises ValueError with "Unknown instruction type requested".
- **Filesystem-service synchronization**: Every .md file in prompts/ (excluding README.md and _code_execution.md variants) must be registered in agent_prompts.path_map.
- **Dead prompt detection**: All prompts registered in PATH_MAP must be used somewhere in the codebase to prevent orphaned prompts.

## Key Quotes
> "assert len(unregistered_files) == 0, f'Found .md files in prompts/ dir not registered in agent_prompts.path_map: {unregistered_files}'"

## Connections
- [[AgentPrompts]] — the service being tested
- [[PATH_MAP]] — the registry mapping prompt types to file paths
- [[PromptBuilder]] — class that uses loaded prompts

## Contradictions
- None identified

---
title: "mvp_site prompt_loader"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/prompt_loader.py
---

## Summary
Prompt variant loading system for dice strategy-specific prompts. Replaces hidden string injection with explicit, version-controlled prompt files.

## Key Claims
- load_prompt_variant() loads prompt file variants based on dice strategy
- Supports dice_strategy options: code_execution, tool_requests, native, native_two_phase
- For code_execution strategy, loads {base_name}_code_execution.md variant
- Falls back to default {base_name}.md for other strategies

## Connections
- [[DiceMechanics]] — strategy determines which prompt variant to load
- [[PromptEngineering]] — version-controlled prompt files for each strategy
---
title: "mvp_site provider_utils"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/provider_utils.py
---

## Summary
Shared utilities for LLM provider implementations. Centralizes tool execution orchestration, dice instruction stripping, schema format helpers, and JSON-first tool requests flow. Schema source of truth is game_state_instruction.md prompt.

## Key Claims
- strip_tool_requests_dice_instructions() removes dice tool_requests sections when using code_execution
- _attach_tool_execution_metadata() attaches dice validation metadata to responses
- get_openai_json_schema_format() provides schema for OpenAI-compatible providers
- run_openai_json_first_tool_requests_flow() handles two-phase JSON-first tool execution
- FACTION_TOOL_NAMES for faction minigame tool filtering

## Connections
- [[LLMIntegration]] — shared provider utilities
- [[FactionMinigame]] — faction tool filtering

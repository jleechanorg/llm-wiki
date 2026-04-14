---
title: "Agent Prompts Module"
type: source
tags: [prompts, llm, schema, prompt-builder, system-instructions]
sources: []
last_updated: 2026-04-14
---

## Summary

Centralized prompt manipulation code for the application. Handles system instruction loading/caching, continuation prompt building, temporal correction prompts, static prompt parts generation, and current turn prompt formatting. Provides schema injection, state example generation, and comment stripping features. llm_service and world_logic delegate prompt construction here.

## Key Claims

- **PATH_MAP Centralization**: Single source of truth mapping prompt types to file paths (narrative, mechanics, dice, game_state, god_mode, etc.)
- **Schema Documentation Cache**: Pre-generates and caches markdown docs for commonly used schema types at startup (CombatState, CombatState, EntityType, CampaignTier, Character, NPC, etc.)
- **Comment Stripping Feature**: Optional ENABLE_PROMPT_COMMENT_STRIPPING env var (default: enabled) removes comment-only content from prompt files
- **State Example Generation**: Runtime injection of schema-consistent examples via `{{STATE_EXAMPLE:TypeName}}` placeholder, prevents prompt-schema drift
- **Schema Placeholder Injection**: Replaces `{{PLANNING_BLOCK_SCHEMA}}`, `{{CHOICE_SCHEMA}}`, `{{VALID_RISK_LEVELS}}`, `{{VALID_CONFIDENCE_LEVELS}}`, `{{VALID_QUALITY_TIERS}}` with actual schema JSON
- **Full Canonical Schema**: `{{FULL_CANONICAL_GAME_STATE_SCHEMA}}` placeholder injects complete game state schema (minified to reduce token overhead)
- **Prompt Order Invariants**: master_directive MUST be first, game_state and planning_protocol MUST be consecutive

## Key Quotes

> "Centralizes ALL prompt manipulation code for the application"

> "Runtime injection of schema-consistent examples into prompts, preventing prompt-schema drift"

> "ENABLE_PROMPT_COMMENT_STRIPPING=false to disable (default: enabled)"

## Connections

- [[AgentArchitecture]] — agent system using these prompts
- [[SchemaValidation]] — schema loading and validation
- [[LLMService]] — llm_service delegates prompt construction here
- [[PromptEngineering]] — prompt building patterns

## Contradictions

- None identified
---
title: "PromptCaching"
type: concept
tags: [prompt-engineering, caching, llm, token-optimization, schema]
sources: [mvp-site-agent-prompts, mvp-site-prompt-loader, mvp-site-prompt-generator]
last_updated: 2026-04-14
---

## Summary

The prompt caching system in WorldAI that separates cacheable (static) from uncacheable (dynamic) request parts to optimize token usage and API costs. The `to_explicit_cache_parts()` function implements explicit cache splitting, ensuring consistent serialization across cache miss scenarios via `build_full_content_for_retry()`.

## Key Claims

### Explicit Cache Splitting
- `to_explicit_cache_parts()` separates static (cacheable) from dynamic (uncacheable) request parts
- Static: system instructions, prompt templates, schema definitions
- Dynamic: game state, entity tracking, user input

### Cache Consistency
- `build_full_content_for_retry()` ensures consistent serialization across cache misses
- Retry logic maintains prompt fidelity after cache failures

### Schema Documentation Cache
- Pre-generates and caches markdown docs for schema types at startup
- Covers: CombatState, EntityType, CampaignTier, Character, NPC, and more
- Prevents repeated schema documentation regeneration

### Comment Stripping
- `ENABLE_PROMPT_COMMENT_STRIPPING` env var (default: enabled)
- Removes comment-only content from prompt files
- Reduces token overhead without losing instruction meaning

### State Example Injection
- `{{STATE_EXAMPLE:TypeName}}` placeholder injects schema-consistent examples at runtime
- Prevents prompt-schema drift between instructions and actual game state

## Connections

- [[PromptEngineering]] — prompt building and optimization
- [[AgentPrompts]] — centralized prompt manipulation
- [[SchemaValidation]] — schema loading and caching
- [[mvp-site-agent-prompts]] — implementation source
- [[mvp-site-prompt-loader]] — prompt variant loading with caching
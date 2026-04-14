---
title: "mvp_site llm_service"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/llm_service.py
---

## Summary
Central AI integration service for WorldArchitect.AI handling story generation, prompt construction, entity tracking, JSON response parsing, model fallback, token management, and agent-based mode routing (StoryModeAgent, GodModeAgent, CombatAgent). Manages ~8000+ lines of LLM orchestration logic with comprehensive error handling.

## Key Claims
- Agent architecture: StoryModeAgent for narrative, GodModeAgent for admin commands, CombatAgent for combat encounters
- Dynamic provider selection with fallback (Gemini -> Cerebras -> OpenRouter) based on API key availability
- Token budget allocation via context_compaction: story_context, core_memories, entity_tracking with OUTPUT_TOKEN_RESERVE (12k default, 24k combat)
- Entity tiering system: ACTIVE/PRESENT/DORMANT tiers for LRU-style token reduction in entity_tracking
- Dice integrity validation: detects narrative fabrication and code execution discrepancies
- Explicit cache splitting: to_explicit_cache_parts() separates cacheable (static) from uncacheable (dynamic) request parts
- Retry logic: build_full_content_for_retry() ensures consistent serialization across cache miss scenarios

## Connections
- [[LLMIntegration]] — orchestrates all AI service calls
- [[GameState]] — game_state included in prompts
- [[EntityTracking]] — entity preloader and validator integrated
- [[ContextCompaction]] — budget allocation and memory management
- [[DiceMechanics]] — dice integrity validation in story generation
- [[FactionMinigame]] — faction state extraction from game_state

---
title: "mvp_site llm_request"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/llm_request.py
---

## Summary
Structured request object for Gemini API calls replacing the flawed json_input_schema approach. Provides flat JSON structure sent directly to the API without string conversion. Implements field ordering strategy optimized for Gemini implicit caching (75% discount on cached tokens).

## Key Claims
- LLMRequest dataclass with core fields: user_action, game_mode, user_id, game_state, story_history, entity_tracking
- to_json() returns flat dictionary with static fields first for cache prefix matching
- build_story_continuation() and build_initial_story() factory methods for common request types
- Payload size validation with MAX_PAYLOAD_SIZE (10MB) and MAX_STRING_LENGTH (1M characters)
- to_explicit_cache_parts() splits into cacheable/uncacheable for explicit caching strategy

## Connections
- [[LLMIntegration]] — structured input to the LLM service
- [[GameState]] — game_state included in request payload
- [[ContextCompaction]] — core_memories processed before sending
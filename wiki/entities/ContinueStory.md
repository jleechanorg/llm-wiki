---
title: "ContinueStory"
type: entity
tags: [function, llm-service, story]
sources: []
last_updated: 2026-04-08
---

## Description
Core function in llm_service.py that continues the game story. Has two implementations:
- continue_story(): Non-streaming path
- continue_story_streaming(): Streaming path (Phase 1/Phase 2)

## Key Behavior
Extracts most recent AI response from story_context and passes to get_agent_for_input for semantic routing.

## Test Coverage
- [[LLM Service Context Extraction Tests]]

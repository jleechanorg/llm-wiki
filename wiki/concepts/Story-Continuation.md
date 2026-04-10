---
title: "Story Continuation"
type: concept
tags: [ai, story-generation, narrative]
sources: [ai-content-personalization-integration-test]
last_updated: 2026-04-08
---

## Overview
AI-generated narrative that continues a story based on user actions and campaign context. Unlike initial story generation, it takes user actions and current game state as input to produce contextually appropriate continuations.

## Key Inputs
- `user_action` — what the player does
- `user_id` — player identifier
- `game_mode` — current mode (story, god, spicy)
- `game_state` — current state including campaign_data
- `story_history` — previous story beats

## Related Pages
- [[AI Content Personalization Integration Test]] — tests continuation with campaign data
- [[LLMRequest]] — builds these requests

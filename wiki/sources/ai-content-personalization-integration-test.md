---
title: "AI Content Personalization Integration Test"
type: source
tags: [python, testing, unittest, integration-test, ai-content, campaign-data]
source_file: "raw/ai-content-personalization-integration-test.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Integration test validating that AI story generation uses campaign data from user campaigns instead of hardcoded content. Tests story continuation and initial story generation with campaign personalization context.

## Key Claims
- **Story Continuation with Campaign Data**: LLMRequest.build_story_continuation correctly integrates campaign_data from game_state including character_name, setting, and description
- **Initial Story Campaign Personalization**: Initial story generation includes campaign-specific context and avoids hardcoded character names
- **No Hardcoded Characters**: Requests do not contain hardcoded names like "Shadowheart", "Ser Arion", "Lyra", or "default character"
- **Campaign Context Accessibility**: campaign_data is accessible in the JSON request structure for story generation

## Key Quotes
> "Test that AI content generation uses user's campaign data" — validates campaign context integration
> "Should not contain hardcoded character names" — ensures personalization over defaults

## Connections
- [[LLMRequest]] — the main class being tested for campaign integration
- [[GameState]] — provides campaign_data context to story requests

## Contradictions
- None identified

---
title: "test_ai_content_simple.py"
type: source
tags: [testing, ai, personalization, campaign-data]
date: 2026-04-14
source_file: raw/mvp_site_all/test_ai_content_simple.py
---

## Summary
Tests that AI story generation uses campaign data from user's campaign instead of hardcoded content. Verifies story continuation integrates campaign context (character name, setting, description) and that hardcoded character names like "Shadowheart" are not present in generated prompts.

## Key Claims
- Story continuation requests include campaign_data in game_state with character_name, setting, and description
- Initial story generation uses user-provided character prompts, not defaults or hardcoded characters
- No hardcoded character names (Shadowheart, Ser Arion, Lyra, default character) should appear in requests
- use_default_world=False ensures campaign-specific context is used

## Key Quotes
> "AI story generation uses campaign data instead of hardcoded content"

## Connections
- [[mvp-site-llm-request]] — LLM request building with campaign context
- [[mvp-site-game-state]] — Game state containing campaign_data

## Contradictions
- None identified in test file
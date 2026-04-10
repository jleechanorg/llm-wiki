---
title: "Main Character Mode"
type: concept
tags: [prompt-mode, player-interaction]
sources: [sariel-v2-campaign-prompts]
last_updated: 2026-04-08
---

## Description
Prompt mode used for all player interactions in the Sariel v2 campaign after initial setup. In main character mode, the LLM generates narrative responses to player inputs while tracking entity states and updating game state.

## Usage in Sariel V2
- interaction_1 through interaction_10: All use main character mode
- Each interaction includes context with location, timestamp, and expected_entities
- Entity tracking is validated across all interactions

## Related Pages
- [[SarielV2CampaignPromptsJune2025]] — Source document
- [[GodMode]] — Opposite mode for initial setup
- [[PromptMode]] — General concept
- [[EntityTracking]] — Core mechanic in this mode

---
title: "God-Mode Directives"
type: concept
tags: [god-mode, game-state, directive, auto-correction]
sources: ["preventing-scene-backtracking-god-mode-corrections"]
last_updated: 2026-04-07
---

## Description
Game master instructions that override normal game state, typically used to correct errors or enforce specific outcomes. The plan specifies detecting these directives in `llm_service.continue_story` prompt and automatically applying them as state deltas before narrative generation.

## Implementation
- Detect in `llm_service.continue_story` prompt prep
- Set `pending_god_mode` flag on `GameState.custom_campaign_state`
- Pre-apply directive as state delta (forced location/time rewrites, inventory tweaks)
- Inject bullet list into system prompt with required acknowledgement field
- Auto-reshot if acknowledgement omitted

## References
- [[GameState]] — stores pending_god_mode flag
- [[LLMService]] — continues story prompt preparation

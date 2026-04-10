---
title: "PromptBuilder"
type: concept
tags: [prompt-engineering, agent, architecture]
sources: ["campaign-settings-tests"]
last_updated: 2026-04-08
---

## Definition
A class in agent_prompts.py responsible for building system instructions for LLM agents. Handles campaign settings, character identity, and god mode directives.

## Key Methods
- `finalize_instructions(parts, use_default_world)` — Adds campaign setting exactly once (production path)
- `build_god_mode_instructions()` — Legacy method for god mode directives
- `_append_campaign_setting_if_present(parts)` — Extracts and appends campaign setting from game_state

## Relevant to
- [[CampaignSettingsTests]] — Tests validate correct behavior of PromptBuilder methods
- [[GameState]] — Provides custom_campaign_state to PromptBuilder

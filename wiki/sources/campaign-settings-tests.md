---
title: "Campaign Settings Tests - Consolidated"
type: source
tags: [python, testing, unittest, campaign-settings, prompt-builder]
source_file: "raw/test_campaign_settings_consolidated.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest suite consolidating three test files for campaign setting handling in agent_prompts.py. Validates that campaign settings appear only once, type guards handle malformed game_state, and god_mode.setting flows to system instructions correctly.

## Key Claims
- **No Duplication**: Campaign setting appears exactly once after finalize_instructions() is called
- **Type Safety**: Type guards prevent AttributeError when custom_campaign_state is None or non-dict
- **System Instruction Flow**: god_mode.setting properly flows to system instructions
- **Production Path**: build_from_order() → finalize_instructions() is the correct production path

## Key Quotes
> "hasattr() returns True if attribute exists even if it's None. The code must check isinstance(dict) before calling .get()." — Type guard requirement

## Connections
- [[PromptBuilder]] — Class being tested for campaign setting handling
- [[GameState]] — The game_state object that holds custom_campaign_state
- [[finalize_instructions]] — Method that adds campaign setting exactly once
- [[buildGodModeInstructions]] — Legacy method that doesn't add campaign setting

## Contradictions
- None identified

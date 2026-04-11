---
title: "Faction Tool Gating Tests"
type: source
tags: [python, testing, faction-minigame, tool-gating, gemini, provider-mocking]
source_file: "raw/test_faction_tool_gating.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests verifying that faction tools are properly gated based on the `faction_minigame.enabled` flag in game state. Tests validate that when the minigame is disabled, faction tools are excluded from the LLM's available toolset, and when enabled, they are included.

## Key Claims
- **Gating Logic**: Faction tools are conditionally available based on `faction_minigame.enabled`
- **Disabled Behavior**: When `enabled=False`, faction tools should NOT be present in the tool list
- **Enabled Behavior**: When `enabled=True`, faction tools should be included alongside dice tools
- **Provider Coverage**: Tests cover Gemini native tools specifically via `generate_content_with_native_tools()`
- **Test Pattern**: Uses mocking for `gemini_provider.get_client` and `_build_gemini_tools`

## Key Quotes
> "Verify Gemini native tools excludes faction tools when enabled=False"

> "Verify Gemini native tools includes faction tools when enabled=True"

## Connections
- [[Faction State Util Module]] — provides `get_faction_minigame_dict()` for extracting state
- [[Faction Settings Persistence]] — related to faction_minigame_enabled setting
- [[Dice Tools and Execution]] — dice tools should always be present regardless of faction state

## Contradictions
- None identified

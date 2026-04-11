---
title: "Faction Test Status - iteration_020"
type: source
tags: [testing, iteration, faction-minigame, tool-invocation, prompt-engineering]
source_file: "raw/worldarchitect.ai-faction_test_status.md"
sources: []
last_updated: 2026-04-07
---

## Summary
Iteration 020 of the faction test status focuses on improving tool invocation rates in LLM behavior for faction status and ranking actions. The test adds explicit warnings about stale cached values, reminder tokens, and forbidden rules to encourage the LLM to call tools rather than use cached game state values.

## Key Claims
- **Prompt Updates**: Added "Cached Values Are Stale" warning section, reminder tokens (`<<CALL-TOOLS-NOW>>`), wrong vs. correct examples, and enhanced forbidden rules
- **Code Changes**: Added tool availability logging in `gemini_provider.py` to track tools passed to API and tools invoked
- **Expected Improvement**: Status actions 0% → 50%+, ranking actions 0% → 50%+, overall 40% → 50%+
- **Test Duration**: 20+ turns with LLM API calls, typically 10-20 minutes

## Key Quotes
> "Cached Values Are Stale" warning at top of prompt — explicit instruction that cached values should not be used

> "Example showing WRONG usage (using cached values)" vs "Example showing CORRECT usage (calling tools first)" — comparative learning examples

## Connections
- [[FactionMinigame]] — the game system being tested
- [[ToolInvocation]] — the core behavior being improved
- [[PromptEngineering]] — methodology used to fix the issue

## Contradictions
- None identified - this iteration builds on iteration_019's 40% baseline

## Entities Mentioned
- `faction_calculate_power` — tool that calculates faction power
- `faction_calculate_ranking` — tool that calculates faction ranking
- `gemini_provider.py` — code file where logging was added
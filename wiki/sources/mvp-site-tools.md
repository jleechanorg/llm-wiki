---
title: "mvp_site tools"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/tools.py
---

## Summary
Faction tool definitions for LLM function calling. Exposes faction Python code as Gemini function tools so backend executes calculations instead of LLM. Pattern follows dice.py: FACTION_TOOLS list + execute_faction_tool() handler.

## Key Claims
- FACTION_TOOL_NAMES: faction_simulate_battle, faction_intel_operation, faction_calculate_ranking, faction_fp_to_next_rank, faction_calculate_power
- faction_simulate_battle for tactical battle simulation
- faction_intel_operation for spy/intel mechanics
- faction_calculate_ranking and faction_fp_to_next_rank for ranking calculations

## Connections
- [[FactionMinigame]] — faction tools as LLM function calling

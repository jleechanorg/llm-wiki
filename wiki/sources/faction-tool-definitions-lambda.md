---
title: "Faction Tool Definitions for LLM Function Calling"
type: source
tags: [llm-function-calling, faction-system, gemini, python, tools]
source_file: "raw/faction-tool-definitions.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module that exposes faction Python code as Gemini function tools, allowing the backend to execute calculations instead of the LLM manually applying formulas from prompts. Follows the same pattern as dice.py with FACTION_TOOLS list and execute_faction_tool() handler.

## Key Claims
- **Backend Execution**: LLM calls tools, backend executes calculations rather than LLM applying formulas
- **Pattern Consistency**: Follows dice.py pattern for tool definitions and routing
- **Tool Routing**: FACTION_TOOL_NAMES canonical set for routing in dice.py and game_state.py
- **Faction Operations**: Five core tools for battle simulation, intel, rankings, and power calculation

## Key Quotes
> "Exposes faction Python code as Gemini function tools so the backend executes calculations instead of the LLM manually applying formulas from prompts."

## Connections
- [[DicePy]] — same pattern for dice tool definitions
- [[GeminiFunctionCalling]] — function calling mechanism used
- [[FactionBattleSim]] — battle simulation module
- [[FactionCombat]] — combat power calculation
- [[FactionIntel]] — intel/spy operations
- [[FactionRankings]] — ranking calculations
- [[SRDUnits]] — Standard Reference Unit definitions

## Contradictions
- []

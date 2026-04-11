---
title: "Faction Tools Schema and Execution Unit Tests"
type: source
tags: [python, testing, faction-minigame, tool-schema, mock-patching]
source_file: "raw/test_faction_tools_schema_execution.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests verifying faction tool schema definitions and execution function mappings. Tests validate tool names, parameter schemas, required fields, and that each tool calls the correct underlying function.

## Key Claims
- **Tool Schemas**: Faction tools have correctly defined JSON schemas with required parameters
- **Schema Validation**: faction_calculate_power requires soldiers, spies, elites; faction_calculate_ranking requires player_faction_power
- **Export Verification**: FACTION_TOOL_NAMES set matches tool names in FACTION_TOOLS
- **Execution Mapping**: Each tool name maps to its corresponding calculation function
- **Mock Pattern**: Tests use unittest.mock.patch to isolate tool execution from backend logic

## Key Quotes
> "Verify faction_calculate_power tool schema is correct."

> "Verify tool calls map to correct functions."

## Connections
- [[Faction Tool Gating Tests]] — validates tool availability based on faction_minigame.enabled flag
- [[Faction State Util Module Unit Tests]] — extracts faction_minigame from game_state
- [[Faction Combat Power Calculation Tests]] — underlying calculation logic

## Contradictions
- None identified

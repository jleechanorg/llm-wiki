---
title: "Planning Block Cleanup - Dev1314"
type: source
tags: [planning-blocks, prompt-cleanup, dev1314, json-first, testing]
source_file: "raw/planning-block-cleanup-dev1314.md"
sources: [game-state-instruction, master-directive, mechanics-system-instruction, narrative-system-instruction]
last_updated: 2026-04-08
---

## Summary
Cleanup of planning block references across prompt template files. Subagents removed narrative-style "--- PLANNING BLOCK ---" delimiters from prompts while preserving JSON field requirements for the planning_block field.

## Key Claims
- **4 prompt files updated** — game_state_instruction.md, master_directive.md, mechanics_system_instruction.md, narrative_system_instruction.md
- **Removed narrative delimiters** — "--- PLANNING BLOCK ---" format no longer appears in prompt text
- **Preserved JSON field requirement** — planning_block remains a required JSON field
- **5 test files analyzed** — comprehensive test coverage for planning block functionality

## Changes Made
1. Line 22: Changed field description from "The --- PLANNING BLOCK ---" to "Character options and choices"
2. Lines 48-60: Removed delimiter format from field description
3. Line 89: Updated to "Put character options in planning_block field"
4. Removed "--- PLANNING BLOCK ---" headers from all template examples

## Test Coverage
- test_planning_block_enforcement.py (757 lines) - comprehensive validation
- test_planning_block_json_corruption_fix.py (170 lines) - JSON parsing
- test_planning_block_json_first_fix.py (96 lines) - JSON-first approach
- test_planning_block_simplified.py (155 lines) - prompt simplification

## Connections
- [[JsonFirstArchitecture]] — the cleaned prompts now enforce JSON-only planning blocks
- [[GameStateInstruction]] — main file updated in this cleanup
- [[TestPlanningBlockEnforcement]] — validates the cleanup works correctly

## Contradictions
- None identified - the cleanup maintains consistency with JSON-first architecture

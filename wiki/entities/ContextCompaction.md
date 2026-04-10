---
title: "ContextCompaction"
type: entity
tags: [python, module, context-management]
sources: ["context-budgeting-allocation-tdd-tests"]
last_updated: 2026-04-08
---

## Description
Python module in mvp_site responsible for managing context budget allocation across system instruction, game state, core memories, entity tracking, and story context components.

## Key Functions
- `_allocate_request_budget` — component-level budget allocation with minimum guarantees
- `_compact_system_instruction` — emergency compaction for oversized system instructions
- `_compact_core_memories` — compaction for core memories exceeding budget
- `_compact_game_state` — compaction for game state JSON exceeding budget
- `_filter_persisted_warnings` — filters warnings for persist_key inclusion

## Constants
- BUDGET_STORY_CONTEXT_ABSOLUTE_MIN — minimum story context tokens
- BUDGET_STORY_CONTEXT_MIN — minimum story context ratio (30%)
- SYSTEM_INSTRUCTION_EMERGENCY_THRESHOLD — 100k tokens triggering emergency compaction

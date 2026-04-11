---
title: "Schema-Prompt Drift Investigation"
type: source
tags: [worldarchitect-ai, schema, prompts, validation, drift, testing]
date: 2026-04-07
source_file: raw/schema-prompt-drift-investigation.md
last_updated: 2026-04-07
---

## Summary
Investigation into hardcoded JSON examples in prompt MD files that drift from the schema over time, causing validation failures in WorldArchitect.AI. Found 59 hardcoded examples across 13 prompt files, with a runtime injection system that only generates type documentation but not example JSON.

## Key Claims
- **59 hardcoded JSON examples** across 13 prompt files cause validation failures when schema evolves
- **Runtime injection system** (`{{SCHEMA:TypeName}}`) exists but only generates type docs, not example JSON
- **Missing fields from schema**: `combat_session_id` (in prompts but not schema), `sanctuary_mode` (object in prompts, boolean in schema)
- **Root cause**: JSON examples manually written, never updated when schema fields added
- **Recommended solution**: Script to extract JSON from schema and generate injection templates

## Hardcoded JSON Distribution

| File | Count |
|------|-------|
| game_state_instruction.md | 20 |
| faction_minigame_instruction.md | 16 |
| rewards_system_instruction.md | 5 |
| game_state_examples.md | 4 |
| god_mode_instruction.md | 3 |
| faction_management_instruction.md | 3 |
| living_world_instruction.md | 2 |
| Other files | 6 |

## Solution Options
1. Add missing fields to schema (quick fix)
2. Replace hardcoded examples with `{{SCHEMA:}}` injection (systematic fix)
3. Add to legacy allowlist in validation (workaround)

## Connections
- [[WorldArchitect.AI]] — the platform this investigation targets
- [[Game State Logical Consistency Validation Test]] — tests that fail due to this drift

## Contradictions
- None identified yet — investigation is new

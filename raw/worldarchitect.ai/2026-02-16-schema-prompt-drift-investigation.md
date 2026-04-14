# Schema-Prompt Drift Investigation

## Problem
Hardcoded JSON examples in prompt MD files are NOT generated from the schema - they drift over time causing validation failures.

## Findings

### Hardcoded JSON Count: 59 examples across 13 prompt files

| File | Count |
|------|-------|
| game_state_instruction.md | 20 |
| faction_minigame_instruction.md | 16 |
| rewards_system_instruction.md | 5 |
| game_state_examples.md | 4 |
| god_mode_instruction.md | 3 |
| faction_management_instruction.md | 3 |
| living_world_instruction.md | 2 |
| think_mode_instruction.md | 1 |
| character_creation_instruction.md | 1 |
| combat_system_instruction.md | 1 |
| deferred_rewards_instruction.md | 1 |
| relationship_instruction.md | 1 |
| reputation_instruction.md | 1 |

### Runtime Injection System (Already Exists)
- `{{SCHEMA:TypeName}}` - generates type docs from schema (works)
- Used in: planning_protocol.md, and some others

### Fields Missing from Schema (Found During Testing)
1. **combat_session_id** - in prompts, NOT in schema
2. **sanctuary_mode** - prompts use object, schema has simple boolean

## Root Cause
- JSON examples in MD files are manually written
- Schema fields added after examples were written never updated the examples
- Runtime injection only generates TYPE documentation, not EXAMPLE JSON

## Solution Options
1. **Add missing fields to schema** - quick fix for specific fields
2. **Replace hardcoded examples with {{SCHEMA:}} injection** - systematic fix
3. **Add to legacy allowlist in validation** - workaround

## Recommendation
Create a script that:
1. Extracts all JSON examples from schema
2. Generates injection templates for each top-level state update type
3. Replaces hardcoded examples in MD files with injection templates

## Evidence
- Test failures: `/tmp/worldarchitectai/schema_followup/schema_validation_real_api-*/`

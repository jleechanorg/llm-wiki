---
title: "Schema-Prompt Drift Investigation"
type: source
tags: [schema, prompt-engineering, validation, json, drift, debugging]
source_file: "raw/schema-prompt-drift-investigation.md"
sources: []
last_updated: 2026-04-07
---

## Summary
Investigation into hardcoded JSON examples in prompt MD files that drift from the schema over time, causing validation failures. Found 59 hardcoded examples across 13 prompt files, with runtime injection system already in place but not fully utilized.

## Key Claims
- **59 hardcoded JSON examples**: Across 13 prompt files, with game_state_instruction.md having 20 examples and faction_minigame_instruction.md having 16
- **Runtime injection exists**: `{{SCHEMA:TypeName}}` generates type docs from schema at runtime (works)
- **Missing fields in schema**: combat_session_id (in prompts but not schema), sanctuary_mode (prompts use object, schema has simple boolean)
- **Root cause**: Manually written JSON examples never updated when schema fields changed

## Key Quotes
> "JSON examples in MD files are manually written" — root cause of drift
> "Runtime injection only generates TYPE documentation, not EXAMPLE JSON" — gap in current system

## Connections
- [[JSON Schema Validation]] — validation failures caused by prompt-schema mismatch
- [[Runtime Injection]] — existing system for schema-derived type docs
- [[Prompt Engineering]] — best practice of generating examples from schema

## Contradictions
- None identified

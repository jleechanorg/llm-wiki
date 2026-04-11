---
title: "JSON Schema Validation Infrastructure for GameState"
type: source
tags: [python, json-schema, validation, game-state, infrastructure, adr]
source_file: "raw/game_state_schema.py"
sources: ["ADR-0003"]
last_updated: 2026-04-08
---

## Summary
Python module providing schema loading, caching, and validation utilities for runtime GameState validation against the canonical JSON Schema. Part of ADR-0003 Phase 2 implementation with custom RFC 3339 datetime format checking.

## Key Claims
- **Schema Caching**: In-memory caching for both schemas and compiled validators to avoid repeated disk I/O and compilation
- **Custom Format Checker**: RFC 3339 datetime validation with pattern matching and isoformat parsing
- **Backward Compatibility**: Legacy field aliases for player character data and equipment slots
- **Validation Message Enrichment**: User-actionable hints for common schema failures like incomplete player_character_data

## Key Quotes
> "JSON Schema validation infrastructure for GameState (ADR-0003 Phase 2)"

## Connections
- [[GameStateSchema]] — the canonical schema this validates against
- [[ADR0003]] — architectural decision record this implements
- [[ValidationModule]] — broader validation context

## Contradictions
- None identified

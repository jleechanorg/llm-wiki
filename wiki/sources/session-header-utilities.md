---
title: "Session Header Utilities"
type: source
tags: [game-state, session-header, utilities, formatting, normalization, player-character, world-data]
source_file: "raw/session-header-utilities.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module providing functions for formatting, normalizing, and generating session headers from game state data. Handles dict-as-string format conversion, prefix normalization, and fallback generation for missing headers.

## Key Claims
- **Safe Data Extraction** — _get_player_character_data and _get_world_data safely extract data from game state objects or dicts with type guards
- **Format Normalization** — normalize_session_header handles dict input, JSON dict-as-string, missing [SESSION_HEADER] prefix, and unsupported types
- **Fallback Generation** — generate_session_header_fallback creates session headers from game_state when LLM omits them
- **Type Coercion** — uses numeric_converters.coerce_int_safe for safe integer conversion

## Functions

### normalize_session_header
Converts session_header to consistent structure:
- Dict input → formatted string
- JSON dict-as-string → parsed and formatted
- Missing [SESSION_HEADER] prefix → prefix added
- Empty/None → empty string

### generate_session_header_fallback
Generates session_header from game_state with:
- Timestamp from world.current_time or world_time
- Location from player character
- Status and conditions
- Resources and health

## Connections
- [[GameState]] — source of player_character_data and world_data
- [[SessionHeader]] — the normalized/generated output format
- [[PlayerCharacterData]] — extracted for location/status
- [[WorldData]] — extracted for timestamp generation

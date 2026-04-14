---
title: "mvp_site validation"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/validation.py
---

## Summary
JSON Schema validation infrastructure for GameState. Provides schema loading, caching, and Draft202012Validator for runtime game state validation against canonical schema.

## Key Claims
- load_schema() loads schema from game_state.schema.json with caching
- validate_game_state() validates against canonical schema
- check_datetime() validates RFC 3339 date-time format
- _SCHEMA_CACHE, _VALIDATOR_CACHE for performance
- LEGACY_CHARACTER_FIELD_ALIASES for backward compatibility

## Connections
- [[GameState]] — schema validation for game state

---
title: "SessionHeaderUtils"
type: concept
tags: [python-module, session-headers, utility-functions]
sources: ["session-header-utils-edge-cases-pr3746"]
last_updated: 2026-04-08
---

## Description
Python module (`session_header_utils.py`) that handles session header generation, normalization, and fallback generation for game state display.

## Key Functions
- `_coerce_int(value, default=0)` — Safely coerce various types to int
- `_get_player_character_data(game_state)` — Extract player character data from dict or object
- `normalize_session_header(header)` — Parse and normalize JSON session headers
- `generate_session_header_fallback(game_state)` — Generate session header from game state

## Related
- [[TypeCoercion]] — pattern used for int conversion
- [[FallbackGeneration]] — pattern for generating defaults from game state
- [[PR3746]] — PR that prompted additional test coverage

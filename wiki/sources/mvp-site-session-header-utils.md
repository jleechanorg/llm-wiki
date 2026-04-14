---
title: "mvp_site session_header_utils"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/session_header_utils.py
---

## Summary
Session Header Utilities for formatting, normalizing, and generating session headers from game state data. Provides _get_player_character_data() and _get_world_data() safe extraction helpers.

## Key Claims
- _get_player_character_data() safely extracts PC data from game state (dict or object)
- _get_world_data() safely extracts world data from game state
- normalize_session_header() for session header normalization
- Guard against non-dict player_character_data

## Connections
- [[GameState]] — session header formatting

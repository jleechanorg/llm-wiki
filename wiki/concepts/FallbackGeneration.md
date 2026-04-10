---
title: "Fallback Generation"
type: concept
tags: [python, defaults, game-state, session-headers]
sources: ["session-header-utils-edge-cases-pr3746"]
last_updated: 2026-04-08
---

## Description
Pattern of generating default values when primary data is unavailable. The `generate_session_header_fallback` function implements this for session headers.

## Key Behaviors
- Uses `hit_dice.total` when `max` key is missing
- Displays class-specific features (Bardic Inspiration, Song of Rest)
- Coerces None values to 0 to prevent TypeError
- Handles both dict and object formats for game state

## Use Case
Provides graceful degradation when Firestore game state is unavailable or malformed, displaying available player information.

## Related
- [[SessionHeaderUtils]] — module implementing fallback generation
- [[DefensiveProgramming]] — broader pattern

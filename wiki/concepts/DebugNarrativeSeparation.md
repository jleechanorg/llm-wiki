---
title: "Debug-Narrative Separation"
type: concept
tags: [testing, debug, quality, narrative]
sources: ["narrative-field-clean-debug-tags", "debug-events-export-tests"]
last_updated: 2026-04-08
---

## Summary
The practice of keeping debug content (state updates, dice roll details, internal reasoning) strictly separated from player-facing narrative text in game responses.

## Key Principles
- **Narrative field**: Only story text visible to players
- **State updates field**: Machine-readable game state changes
- **Debug info field**: DM notes and internal reasoning (hidden from players)

## Forbidden Patterns in Narrative
- `[DEBUG_START]` / `[DEBUG_END]`
- `[DEBUG_STATE_START]` / `[DEBUG_STATE_END]`
- `[DEBUG_ROLL_START]` / `[DEBUG_ROLL_END]`
- `[STATE_UPDATES_PROPOSED]` / `[END_STATE_UPDATES_PROPOSED]`

## Why It Matters
Debug content in narrative breaks immersion and can expose internal game mechanics to players. Tests verify this separation is maintained.

## Related Concepts
- [[LLMResponse Structured Fields]]
- [[Debug Events Export]]

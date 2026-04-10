---
title: "Character Creation Mode"
type: concept
tags: [game-mode, character, narrative-generation]
sources: []
last_updated: 2026-04-08
---

## Definition
A game mode in the OpenClaw system where the LLM generates character creation narrative immediately after a character is defined. The character data is passed via god_mode_data (string format from frontend).

## Key Properties
- **Trigger**: Character data provided in god_mode_data field
- **Expected output**: Immediate character creation narrative on Turn 0
- **Bug symptom**: Shows placeholder "[Character Creation Mode - Story begins after character is complete]" instead of generated narrative

## Related Concepts
- [[God Mode]] — the parent feature that enables character creation mode
- [[Turn 0]] — the game turn where character creation narrative should appear

## Known Issues
- god_mode_data (string) must be parsed into god_mode (dict) for is_god_mode_with_character check to pass

---
title: "Turn 0"
type: concept
tags: [game-turn, character-creation, narrative]
sources: []
last_updated: 2026-04-08
---

## Definition
The first game turn (Turn 0) in OpenClaw where the opening story/narrative is generated. For God Mode campaigns with character data, this should produce character creation narrative immediately.

## Behavior
- **Normal campaigns**: Opening story generated based on campaign setup
- **God Mode campaigns**: Should show character creation narrative if character data provided
- **Bug**: Shows placeholder text instead of generated narrative when god_mode_data string is not parsed

## Related Concepts
- [[Character Creation Mode]] — the mode that should trigger on Turn 0
- [[God Mode]] — the feature enabling character-based narrative generation

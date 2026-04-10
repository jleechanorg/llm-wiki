---
title: "Scene Numbering"
type: concept
tags: [game-state, ui-display, scene-tracking]
sources: []
last_updated: 2026-04-08
---

## Definition
A user-facing counter that displays the current scene number to players. In OpenClaw, scene numbers only increment for AI (Gemini) responses, not user inputs.

## Key Properties
- **user_scene_number**: Player-visible "Scene #X" counter
- Only increments for AI responses (actor = "gemini")
- User inputs receive user_scene_number=None
- Approximate relationship: user_scene_number ≈ turn_number / 2

## Related Concepts
- [[TurnCounter]] - Internal counter for all story entries
- [[SequenceID]] - Absolute position in story array
- [[StoryEntry]] - Individual entries in story history

## Use Case
Prevents confusion from seeing scene numbers that appear to skip values (e.g., Scene 1, 2, 5, 6 instead of 1, 2, 3, 4).

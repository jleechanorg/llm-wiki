---
title: "Turn Counter"
type: concept
tags: [game-state, turn-tracking, internal-counter]
sources: []
last_updated: 2026-04-08
---

## Definition
Internal counter tracking all story entries (user inputs + AI responses). Used for game state management and analytics.

## Key Properties
- **turn_number**: Counts ALL story entries regardless of actor
- Increments for both user inputs and AI responses
- Different from user-facing scene numbers

## Relationship to Scene Numbering
- Turn counter is internal; scene numbering is user-facing
- Scene number ≈ turn number / 2 (when alternating user/AI)
- Turn counter preserves full history; scene number shows progression

## Related Concepts
- [[SceneNumbering]] - User-facing display
- [[SequenceID]] - Absolute array position
- [[StoryEntry]] - Individual entry record

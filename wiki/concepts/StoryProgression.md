---
title: "Story Progression"
type: concept
tags: [story, turns, scenes, counting]
sources: [llm-service-ai-integration-response-processing]
last_updated: 2026-04-08
---

Distinct counting systems used in the codebase for tracking story progression through different metrics.

## Counting Systems
- **story_entry_count / turn_number**: Internal counter of ALL story entries (both user inputs and AI responses). Calculated as `len(story_context) + 1`. Used for caching and entity manifest tracking.

- **sequence_id**: Absolute position in story array. Every entry (user + AI) gets an incrementing sequence_id. Technical identifier for ordering.

- **user_scene_number**: User-facing "Scene #X" counter. ONLY increments for AI (Gemini) responses. User inputs get user_scene_number=None. This is what players see as scene progression.

## Relationship
Approximate relationship (assumes perfect alternation):
`user_scene_number ≈ story_entry_count / 2`

## Example
With 6 entries alternating user/AI:
- Entry 1: user → sequence_id=1, user_scene_number=None
- Entry 2: gemini → sequence_id=2, user_scene_number=1 (Scene #1)
- Entry 3: user → sequence_id=3, user_scene_number=None
- Entry 4: gemini → sequence_id=4, user_scene_number=2 (Scene #2)
- Entry 5: user → sequence_id=5, user_scene_number=None
- Entry 6: gemini → sequence_id=6, user_scene_number=3 (Scene #3)

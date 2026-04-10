---
title: "Turn vs Scene"
type: concept
tags: [numbering, protocol, worldarchitect]
sources: [game-state-management-protocol]
last_updated: 2026-04-08
---

Turn vs Scene distinction defines how numbering works in WorldArchitect.AI for user-facing vs internal counters.

**Definitions**:
- **turn_number / story_entry_count**: Internal counter for every story entry (user + AI). Absolute order of exchanges.
- **sequence_id**: Absolute index in stored story array (mirrors turn_number but can be remapped during replay).
- **user_scene_number**: User-facing "Scene #X" that increments ONLY on AI (Gemini) responses. Stays `null` on user inputs.

**Approximation**: When conversation alternates perfectly, `user_scene_number` ≈ `turn_number / 2`

**Related Concepts**:
- [[GameStateManagement]] — overall state protocol
- [[VisibilityRule]] — what players see

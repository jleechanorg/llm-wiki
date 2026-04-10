---
title: "Story Context"
type: concept
tags: [game-state, timeline, data-structure]
sources: [timeline-log-budget-end2end-tests]
last_updated: 2026-04-08
---

The chronological history of player actions and GM responses in a campaign. Stored as an array of turn objects with actor, text, and sequence_id fields. Grows with each interaction and is a primary input to LLM prompts.

## Structure
```python
[
  {"actor": "player", "text": "I examine the runes", "sequence_id": 1},
  {"actor": "gm", "text": "The runes glow with ancient power", "sequence_id": 2},
]
```

## Budget Considerations
- Large story_contexts (80+ turns) can trigger guardrails
- Dormant duplication guard prevents false timeline entries
- Timeline_log budgeting ensures memory-efficient handling

## Connections
- [[GameState]] — contains story_context field
- [[Timeline Log Budget Guardrails]] — manages context size

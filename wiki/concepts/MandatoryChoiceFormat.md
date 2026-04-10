---
title: "Mandatory Choice Format"
type: concept
tags: [ui-pattern, modal-agent, choice-interface]
sources: ["character-creation-level-up-mode"]
last_updated: 2026-04-08
---

UI/UX pattern requiring every agent response to include explicit planning_block with choices. Ensures users always have clear navigation options and cannot accidentally escape modal flows through semantic inputs.

## Implementation
```json
{
  "planning_block": {
    "thinking": "Current status summary",
    "choices": {
      "option_1": {"text": "...", "description": "..."},
      "option_2": {"text": "...", "description": "..."}
    }
  }
}
```

Used by [[CharacterCreationAgent]] to enforce exit choice availability.

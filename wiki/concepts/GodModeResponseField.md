---
title: "God Mode Response Field"
type: concept
tags: [god-mode, frontend-integration, response-schema]
sources: ["god-mode-response-field-tests"]
last_updated: 2026-04-08
---

A specific field in the structured JSON response used for god mode content.

## Description
The god_mode_response field is used when the LLM response is in god mode (correction/override mode). Unlike the narrative field which contains the main story text, god_mode_response contains:
- Environmental descriptions
- NPC introductions
- State modifications
- DM notes

When this field is present and non-empty, the frontend should use it directly instead of the narrative field.

## Usage
```python
narrative, response_obj = parse_structured_response(god_response)
# response_obj.god_mode_response contains the god mode content
```

## Related Concepts
- [[ParseStructuredResponse]] - The parsing function
- [[GodMode]] - The game mode itself

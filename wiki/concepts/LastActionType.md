---
title: "LastActionType"
type: concept
tags: [game-state, action-tracking, agent-selection]
sources: []
last_updated: 2026-04-08
---

## Description
Game state attribute that tracks the most recently executed action type (e.g., "persuasion", "combat", "exploration"). Used by agents to determine appropriate behavior based on recent player actions.

## Known Issue
The current DialogAgent implementation does not properly trigger on "persuasion" as a last_action_type value.

## Related
- [[DialogAgent]] should respond to this for dialog continuity
- [[GameState]] maintains this attribute

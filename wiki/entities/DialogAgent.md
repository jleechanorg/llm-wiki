---
title: "DialogAgent"
type: entity
tags: [agent, dialog, llm, game-state]
sources: []
last_updated: 2026-04-08
---

## Description
Agent responsible for handling dialog state continuity and character-focused conversations. Selected when game is in dialog state or explicit dialog mode is requested.

## Key Methods
- `matches_game_state(game_state)` — determines if DialogAgent should be active based on game state (dialog_context, last_action_type, is_in_combat, planning_block)

## Related Tests
- [[DialogAgent E2E tests validate agent selection and system instruction filtering]]
- [[DialogAgent persuasion action bug reproduction]]

## Known Issues
- Does not currently trigger on "persuasion" action type — bug reproduced in test

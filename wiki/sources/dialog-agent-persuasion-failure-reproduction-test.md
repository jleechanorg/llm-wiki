---
title: "DialogAgent persuasion action failure reproduction test"
type: source
tags: [python, testing, dialog-agent, agent-selection, bug-reproduction]
source_file: "raw/test_dialog_agent_persuasion_failure.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit test that reproduces a reported bug where DialogAgent fails to activate after a "persuasion" action. The test expects `DialogAgent.matches_game_state()` to return `True` when `last_action_type` is "persuasion", but the current implementation likely returns `False`.

## Key Claims
- **Persuasion Trigger**: DialogAgent should activate when `last_action_type` is "persuasion"
- **Current Behavior**: Likely returns `False` after persuasion action (bug)
- **Expected Behavior**: `matches_game_state()` should return `True` for persuasion actions

## Test Logic
The test creates a mock GameState with:
- `is_in_combat()` returns `False`
- `dialog_context` is inactive (`{"active": False}`)
- `planning_block` is empty
- `last_action_type` is set to "persuasion"

The assertion expects `DialogAgent.matches_game_state(mock_game_state)` to return `True`.

## Connections
- [[DialogAgent]] — the agent being tested
- [[GameState]] — the game state class
- [[DialogAgent E2E tests validate agent selection and system instruction filtering]] — related E2E tests

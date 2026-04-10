---
title: "LevelUpActiveStateLogic"
type: concept
tags: [level-up, state-management, agent-routing, modal]
sources: ["rev-0g1y-level-up-active-state-inconsistency"]
last_updated: 2026-04-08
---

## Definition
Logic that determines whether a character is currently in a level-up flow, used to route requests to `LevelUpAgent` and inject modal finish choices.

## Key Components
- `get_agent_for_input` — determines which agent handles input based on game state
- `_inject_modal_finish_choice_if_needed` — injects "finish level-up" choice into planning blocks

## Stale Flags
- `level_up_in_progress` — explicit flag indicating level-up flow is active
- `level_up_pending` — flag indicating level-up is available but not yet started
- `rewards_pending.level_up_available` — indicates rewards that include level-up

## Issue (REV-0g1y)
`get_agent_for_input` and `_inject_modal_finish_choice_if_needed` used different logic to detect active level-up state, causing:
- Routing may not activate modal while injection adds finish choice
- Stale flags (`level_up_in_progress=False`) not respected by injection logic

## Related
- [[ModalInjection]] — the injection mechanism
- [[StaleFlagGuard]] — pattern for handling stale state

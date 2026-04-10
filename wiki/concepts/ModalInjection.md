---
title: "ModalInjection"
type: concept
tags: [modal, injection, planning-block, game-state, ui]
sources: ["rev-0g1y-level-up-active-state-inconsistency"]
last_updated: 2026-04-08
---

## Definition
The mechanism by which the game system injects special choices (like "finish level-up") into planning blocks based on game state conditions.

## Key Function
`_inject_modal_finish_choice_if_needed` — inspects game state to determine if modal finish choice should be added to the planning block's choices.

## Injection Conditions
- Must check `level_up_in_progress` stale guard
- Must check `level_up_pending` stale guard  
- Must check `rewards_pending.level_up_available`

## The Bug (REV-0g1y)
The injection function did not check `level_up_in_progress` or `level_up_pending` stale flags, causing finish choices to be injected even when the level-up flow was explicitly cleared.

## Related
- [[LevelUpActiveStateLogic]] — determines when injection is needed
- [[PlanningBlock]] — the structure being modified by injection

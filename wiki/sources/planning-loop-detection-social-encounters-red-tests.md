---
title: "Planning Loop Detection for Social Encounters — RED Test"
type: source
tags: [python, testing, red-test, planning-block, social-encounters, loop-detection]
source_file: "raw/test_planning_loop_social_encounters.py"
sources: [game_state_instruction.md]
last_updated: 2026-04-08
---

## Summary
RED (failing) test that reproduces a bug where social encounters get stuck in planning loops without dice rolls or resolution. Tests validate that the Anti-Loop Rule enforces execution after repeated similar actions, and that social encounters require skill checks with dice rolls.

## Key Claims
- **Social action bad response structure**: Documents problematic pattern where LLM describes situation without rolling dice or requesting tool checks
- **Anti-Loop Rule enforcement**: After 2+ similar user actions, system MUST execute with dice roll — never present third round of options
- **Dice roll required for social resolution**: Social encounters (persuasion, intimidation, deception) require skill checks with dice rolls to progress narrative
- **Bug reproduction**: User selected variants of "Press Logical Argument" 6+ times (Scenes 257-264) without resolution

## Key Quotes
> "User selects a social action, LLM describes the situation but doesn't roll dice, LLM presents same/similar options again, Loop repeats indefinitely"

> "Action Execution Rule (game_state_instruction.md line 239-244): EXECUTE the chosen action with dice rolls, DO NOT present more sub-options"

> "Anti-Loop Rule: If same action selected twice, ALWAYS execute on second selection"

## Connections
- [[ActionExecutionRule]] — referenced from game_state_instruction.md line 239-244
- [[Reynolds]] — Agent example in test narrative
- [[AntiLoopRule]] — rule that should force execution after repeated similar actions
- [[SocialEncounter]] — encounter type that requires skill checks
- [[DiceRoll]] — required outcome for social action resolution

## Contradictions
- None identified yet — this is a RED test documenting current broken behavior

---
title: "Action Execution Rule"
type: entity
tags: [rule, game-mechanic, game-state-instruction]
sources: [planning-loop-detection-social-encounters-red-tests.md, game_state_instruction.md]
last_updated: 2026-04-08
---

## Summary
Game rule from game_state_instruction.md (lines 239-244) that mandates executing chosen actions with dice rolls rather than presenting more sub-options.

## Definition
- **Execute the chosen action** with dice rolls
- **Do NOT present more sub-options** once an action is selected
- **Anti-Loop Rule**: If same action selected twice, ALWAYS execute on second selection

## Connection to Bug
The RED test reproduces a violation of this rule where:
1. User selects social action (e.g., "Press the Logical Argument")
2. LLM describes situation but doesn't roll dice
3. LLM presents same/similar options again (violates "do not present more sub-options")
4. Loop repeats indefinitely

## Connections
- [[AntiLoopRule]] — enforcement mechanism for this rule
- [[PlanningLoopDetection]] — test that validates this rule is enforced
- [[GameStateInstruction]] — source document for this rule

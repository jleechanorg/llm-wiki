---
title: "Social Encounter"
type: concept
tags: [encounter-type, game-mechanic, skill-check]
sources: [planning-loop-detection-social-encounters-red-tests.md]
last_updated: 2026-04-08
---

## Summary
A game encounter type involving NPC interaction through social skills (persuasion, intimidation, deception, etc.) that requires skill checks with dice rolls to resolve.

## Requirements for Resolution
- **Skill check required**: Social actions must request a tool/skill check
- **Dice roll required**: Must include dice_rolls in the response
- **No sub-options after selection**: Per [ActionExecutionRule](../entities/ActionExecutionRule.md), do not present more sub-options once action is selected

## Types of Social Skills
- Persuasion
- Intimidation
- Deception
- Insight (reading NPC)
- Performance (social performances)

## Bug Context
Social encounters are affected by [PlanningLoopDetection](PlanningLoopDetection.md) bug where LLM doesn't execute skill checks or roll dice.

## Connections
- [PlanningLoopDetection](PlanningLoopDetection.md) — bug affecting social encounters
- [DiceRoll](DiceRoll.md) — required for social resolution
- [SkillCheck](SkillCheck.md) — mechanism for social actions
- [ToolRequests](ToolRequests.md) — how skill checks are requested

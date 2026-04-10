---
title: "Dice Roll"
type: concept
tags: [game-mechanic, resolution, skill-check]
sources: [planning-loop-detection-social-encounters-red-tests.md]
last_updated: 2026-04-08
---

## Summary
Game mechanic required to resolve actions, especially social encounters. Dice rolls must be included in LLM responses when actions require skill checks.

## Requirement for Social Encounters
Social encounters (persuasion, intimidation, deception) require dice rolls to progress the narrative. The test asserts that:
- A BAD response has no dice_rolls for social action
- A GOOD response includes dice rolls for skill checks

## In Response Structure
```python
{
    "narrative": "...",
    "dice_rolls": [...],  # REQUIRED for social resolution
    "tool_requests": [...],  # REQUIRED for skill checks
    "planning_block": {...}
}
```

## Bug Context
The planning loop bug occurs because LLM omits dice_rolls for social actions, causing the loop.

## Connections
- [[SocialEncounter]] — requires dice rolls
- [[PlanningLoopDetection]] — bug where dice rolls are missing
- [[AntiLoopRule]] — forces dice roll on second similar action
- [[SkillCheck]] — paired with dice roll for resolution

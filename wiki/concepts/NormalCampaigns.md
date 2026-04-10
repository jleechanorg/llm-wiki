---
title: "Normal Campaigns"
type: concept
tags: ["campaign-type", "game-mode"]
sources: ["llm-first-state-management-plan-pr-2778"]
last_updated: 2026-04-07
---

# Normal Campaigns

## Definition
Standard campaign type in WorldArchitect.AI where players experience a linear D&D narrative.

## State Variables
- Character gold (character.gold)
- Character level (character.level)
- Character XP (character.xp)
- World time (world_time)
- Location, HP, conditions, exhaustion

## Key Point
Normal campaigns use the **exact same LLM narrative generation path** as faction campaigns. The coherence issues would affect both campaign types because they stem from the same LLM narrative generation logic.

## Related Issues
- Timestamp inconsistencies (same as faction)
- Gold calculation errors (same as faction)
- Level progression gaps (same as faction)
- Issues appear after 15+ scenes due to LLM drift

---
title: "Beads"
type: entity
tags: [issue-tracking, evaluation-feedback, game-state]
sources: [manual-beads-creation-guide]
last_updated: 2026-04-07
---

## Overview
Beads is an issue tracking system used for managing evaluation feedback and game state bugs in what appears to be a D&D-style campaign game. Issues are categorized by priority (1-3) with Priority 1 being critical bugs affecting gameplay integrity.

## Key Issues Tracked
- **Context Hallucination** (Priority 1): AI responding to wrong entities from previous scenes
- **Monotonic Counter Validation** (Priority 1): Ensuring XP, gold, territory never decrease
- **FP/Gold Transparency** (Priority 2-3): Displaying calculation breakdowns
- **Character Progression** (Priority 2-3): HP, Hit Dice, XP pacing
- **Economic Balancing** (Priority 3): Income formulas, upkeep costs

## Related Concepts
- [[GameStateManagement]] — overall game state handling
- [[PromptEngineering]] — reducing hallucinations via prompts
- [[CampaignCoherence]] — maintaining narrative consistency

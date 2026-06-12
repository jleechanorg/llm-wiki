---
title: "Beads"
type: entity
tags: [issue-tracking, evaluation-feedback, game-state]
sources: [manual-beads-creation-guide]
last_updated: 2026-06-12
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

## Operational Pattern: Executable Follow-up Beads

As of 2026-06-12, PR/code-review follow-up beads should include exact source context, current SHA, file/line evidence, actual API/function signatures copied from live code, call-site examples, standards constraints, verification commands, and a staleness note. The reusable skill is `/Users/jleechan/.claude/skills/bead-followup-templates/SKILL.md`.

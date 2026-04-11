---
title: "LLM-First State Management Plan"
type: source
tags: [worldarchitect.ai, state-management, coherence, prompt-engineering, faction-minigame, game-state]
sources: []
date: 2026-04-07
last_updated: 2026-04-07
---

## Summary

PR #2778 introduces an LLM-first approach to campaign coherence, replacing server-side state validation with improved prompt engineering. The plan addresses timestamp inconsistencies, gold calculation errors, and level progression gaps that emerge after 15+ scenes. Key principle: "Let LLM manage state through better instructions, context, and structured output. Server-side fixes only for critical safety."

## Key Claims

- **Both Normal and Faction Campaigns Affected**: Same LLM service, same narrative generation path, same state management — fixes benefit both campaign types
- **Root Cause: LLM Drift Over Long Sequences**: Issues appear after Scene 14; 5-turn tests didn't catch coherence problems
- **Primary Fix: Prompt Engineering**: Add state coherence requirements to prompts covering timestamps, gold, and level progression
- **Dual Gold Tracking Clarity**: Faction campaigns track `character.gold` (personal) and `faction.resources.gold` (treasury) separately
- **Server-Side Fixes Reserved**: Only for critical safety, not general state validation

## Key Quotes

> "Let LLM manage state through better instructions, context, and structured output. Server-side fixes only for critical safety."

> "Normal campaigns use the exact same LLM narrative generation path as faction campaigns. The coherence issues would affect both campaign types."

## Problems Identified

1. **Timestamp Inconsistencies**: Scene 14→15 jumps 08:05→10:45, Scene 20→21 reverses 11:15→10:45
2. **Gold Calculation Errors**: Scene 18 shows 110gp (should be 10gp)
3. **Level Progression Gaps**: Character jumps Level 1→3 without showing Level 2
4. **Tutorial Completion Timing**: "Tutorial complete" appears mid-campaign but gameplay continues

## Implementation Strategy

### Priority 1: Prompt Engineering

#### State Coherence Requirements

**Timestamp Tracking Rules**:
- Small actions: +5-15 minutes
- Combat actions: +30-60 minutes  
- End turn: +7 days (advance to next week)
- NEVER go backwards in time

**Gold Calculation Rules**:
- Always calculate: Previous Gold - Costs + Rewards = New Gold
- Show calculation before narrative
- Faction Mode: Track BOTH character.gold AND faction.resources.gold separately

**Level Progression Rules**:
- Show progression incrementally: Level 1 → Level 2 → Level 3
- Never skip levels
- Include XP tracking
- Show level-up message BEFORE applying level

## Connections

- [[Iteration 007 Final Campaign Analysis]] — documents the 25-turn E2E test that exposed coherence issues
- [[WorldAI Faction Management Mini-Game Tests]] — validates faction minigame state structure

## Contradictions

- Contradicts server-side state validation approaches: this plan favors LLM-first over enforcement

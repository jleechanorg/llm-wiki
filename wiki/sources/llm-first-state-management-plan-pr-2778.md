---
title: "LLM-First State Management Plan (PR #2778)"
type: source
tags: ["llm", "state-management", "campaign-coherence", "prompt-engineering", "pr-2778", "timestamp", "gold", "level"]
date: 2026-04-07
source_file: "raw/llm_wiki-raw-worldarchitect.ai-llm_state_management_plan.md"
sources: []
last_updated: 2026-04-07
---

## Summary
PR #2778 introduces an LLM-first approach to campaign coherence, replacing server-side state validation with improved prompt engineering. The plan addresses timestamp inconsistencies (Scene 14-15 jumps 08:05-10:45), gold calculation errors (shows 110gp when should be 10gp), and level progression gaps (Level 1-3 without Level 2) that emerge after 15+ scenes. Core principle: "Let LLM manage state through better instructions, context, and structured output. Server-side fixes only for critical safety." Both normal and faction campaigns share the same LLM path, so fixes benefit both.

## Key Claims
- **Both campaign types affected**: Normal and faction campaigns use the same LLM path, so state coherence fixes benefit both
- **Faction exposes issues more readily**: Longer sequences (20-turn test generates 25+ scenes) and more complex state (dual gold tracking) make issues more visible
- **Root cause is LLM drift**: Issues appear after 15+ scenes due to cumulative drift in LLM state management
- **Prompt engineering is primary fix**: Add state coherence requirements to prompts rather than server-side validation
- **Dual gold tracking complexity**: Faction mode tracks both character.gold (personal) and faction.resources.gold (faction treasury) separately
- **Server-side fixes only for critical safety**: LLM improvements are the primary approach, server validation only for safety-critical issues

## Key Quotes
> "Let LLM manage state through better instructions, context, and structured output. Server-side fixes only for critical safety." — Core principle

> "Normal campaigns use the exact same LLM narrative generation path as faction campaigns." — Shared LLM Path section

## Implementation Details

### Timestamp Tracking Rules
- **Always advance time logically** from previous timestamp
- Small actions (build, recruit): +5-15 minutes
- Combat actions: +30-60 minutes
- End turn: +7 days (advance to next week)
- **NEVER go backwards in time**
- If previous was `08:05`, next must be `>= 08:05`

### Gold Calculation Rules
- **Always calculate**: Previous Gold - Costs + Rewards = New Gold
- **Show calculation before narrative**
- **Faction Mode**: Track BOTH character.gold (personal) AND faction.resources.gold (faction treasury) separately
- Building costs: Farms (100gp), Libraries (100gp), Training Grounds (100gp), etc.
- Combat rewards: Vary by battle outcome (typically 200-800gp)

### Level Progression Rules
- **Show progression incrementally**: Level 1 → Level 2 → Level 3
- **Never skip levels** (no 1 → 3 jumps)
- Include XP tracking: "Level 2 (XP: 300/900)"
- Show level-up message **before** applying level

## Connections
- [[PR2778]] — This PR implements the LLM-first state management plan
- [[GameState]] — The GameState object that tracks character gold, level, world time
- [[TimestampTracking]] — Concept for tracking logical time progression in narratives
- [[GoldCalculation]] — Concept for calculating gold changes correctly
- [[FactionCampaigns]] — Faction campaigns expose issues more due to dual gold tracking
- [[NormalCampaigns]] — Normal campaigns affected by same underlying coherence issues
- [[WorldArchitectAI]] — The platform this plan improves

## Contradictions
- None identified yet — this is a new source documenting planned fixes
---
title: "LLM-First State Management Plan"
type: source
tags: [worldarchitect, state-management, llm, prompts, campaign]
date: 2026-01-12
source_file: raw/worldarchitect.ai/llm_state_management_plan.md
---

## Summary
PR #2778 plan for fixing campaign coherence issues (timestamp inconsistencies, gold calculation errors, level progression gaps) through LLM-first improvements. Core principle: let LLM manage state through better instructions, context, and structured output — server-side fixes only for critical safety. Four-phase implementation: prompt engineering, context management, structured output, minimal server safeguards.

## Key Claims
- **Core Principle**: Let LLM manage state through better instructions — server-side only for critical safety
- **Root Cause**: LLM drift over long sequences (15+ scenes). 5-turn tests don't catch what appears after Scene 14.
- **Dual Gold Tracking**: Faction campaigns have TWO separate pools: `character.gold` (personal) and `faction.resources.gold` (faction treasury). LLM may confuse these.
- **Four Phases**: (1) Prompt Engineering (highest impact, lowest risk), (2) Context Management, (3) Structured Output, (4) Minimal Server Safeguards
- **Success Targets**: Phase 1: 50%+ resolved, Phase 2: 80%+, Phase 3: 90%+, Phase 4: 95%+
- **Critical Discovery**: Scene 18 gold error likely LLM confusing dual gold pools
- **Fallback**: If LLM-first approach doesn't achieve 80%+ after Phase 2, re-evaluate to hybrid approach

## Key Quote
> "Let LLM manage state through better instructions, context, and structured output. Server-side fixes only for critical safety."

## Phase 1: Prompt Engineering
- State Coherence Requirements (timestamp never goes backwards, show gold calculation before narrative, incremental level progression)
- Chain-of-Thought State Tracking (show calculations before narrative)
- Self-Validation Checklist (verify before finalizing response)
- Dual Gold Clarification (explicit character.gold vs faction.resources.gold)

## Phase 2: Context Management
- State Summary Injection (inject current state before each LLM call)
- Recent State History (last 3 scenes)
- Progressive Context Refresh (every 5 scenes)
- Action-to-State Mapping Rules table

## Phase 3: Structured Output
- State Update Schema requiring JSON with state_updates + narrative
- Enforce in prompts

## Phase 4: Server Safeguards (last resort)
- Bounds checking (gold >= 0, level 1-20)
- Retry logic (max 2 retries with enhanced instructions)
- Logging for analysis

## Connections
- [[WorldArchitect.AI]] — PR #2778 for campaign coherence fixes
- [[CampaignCoherence]] — core issue: long-sequence LLM drift
- [[LLMDrift]] — root cause of coherence failures over 15+ scenes
- [[TimestampTracking]] — timestamp progression rules
- [[GoldCalculation]] — dual gold tracking in faction campaigns
- [[StructuredResponseFields]] — structured output approach

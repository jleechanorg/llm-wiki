---
title: "LLM Drift"
type: concept
tags: [llm, drift, consistency, context]
sources: []
last_updated: 2026-04-07
---

## Description
Phenomenon where LLM-generated content loses consistency over longer sequences, causing rule violations that were previously fixed.

## Symptoms
- Timestamp reversals (fixed in Phase 1)
- Level jumps (Level 2→5 at Scene 24→25)
- Gold calculation errors
- State inconsistencies

## Root Cause
Context window pressure over 15+ scenes causes LLM to lose focus on injected rules.

## Solutions
- **Phase 1**: Prompt clarifications (works for early scenes)
- **Phase 2**: State summary injection mid-campaign
- **Phase 3**: Structured output with validation
- **Phase 4**: Server-side rule enforcement


## Connections
- [[20TurnTestImprovementSummary]] — observed at Scene 24→25
- [[ContextManagement]] — solution approach
- [[TimestampProgression]] — also affected by drift

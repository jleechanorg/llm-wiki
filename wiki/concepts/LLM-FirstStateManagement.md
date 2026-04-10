---
title: "LLM-First State Management"
type: concept
tags: ["llm", "state-management", "prompt-engineering"]
sources: ["llm-first-state-management-plan-pr-2778"]
last_updated: 2026-04-07
---

# LLM-First State Management

## Definition
An approach to campaign state coherence that relies on LLM instructions, context, and structured output rather than server-side validation.

## Core Principle
> "Let LLM manage state through better instructions, context, and structured output. Server-side fixes only for critical safety."

## Implementation
1. **Prompt Engineering** (Primary): Add state coherence requirements to prompts
2. **Server-Side Validation** (Secondary): Only for critical safety issues


## Benefits
- Reduces server-side validation complexity
- Leverages LLM's understanding of narrative flow
- Works for both normal and faction campaigns
- Addresses root cause rather than symptoms

## Related Issues
- Timestamp inconsistencies
- Gold calculation errors
- Level progression gaps
- State drift over long sequences (15+ scenes)

---
title: "Context Management"
type: concept
tags: [context, state, llm, drift, memory, AI-attention, token-optimization]
sources: ["openai-harness-ryan-notes"]
last_updated: 2026-04-08
---

## Two Fundamental Constraints

### 1. What's In Context
- How much information can fit in the model's context window
- Context exhaustion largely solved via compaction (GPT-4.5/5.4)
- Allows sessions running 6, 12, 24 hours continuously

### 2. What's the Attention of the Model
- When given too many concurrent directives, attention fragments
- Quality degrades as primary output suffers
- The new frontier challenge

## The "Side Quest" Paradigm

When a human encounters a necessary refactor while building a feature:
- Do I derail to fix it now?
- Or log a ticket for later?

With AI, parallelism is cheap:
1. Primary agent logs the desired change
2. Fork off entirely separate, specialized agent
3. Handle "side quest" while preserving main agent's focus
4. Both improvements happen simultaneously

## Progressive Disclosure

### Persona-Oriented Docs
- Stay small and principle-based
- Just-in-time reasoning for specific implementation
- Agent figures out which docs are relevant

### Just-in-Time Learning
- Agent learns on the job each session
- Already has helpful set of guides
- Can focus on right area of codebase

## LLM Drift (Historical Context)
LLMs lose consistency after 15+ scenes due to context window pressure. Solutions progress from least invasive to most invasive:

- **Phase 1**: Prompt fixes
- **Phase 2**: State summary injection (recommended for 15+ scenes)
- **Phase 3**: Structured output validation
- **Phase 4**: Server-side safeguards (last resort)

## Connections
- [[HarnessEngineering]] - Using context files effectively
- [[DualAgentArchitecture]] - Attention separation
- [[LLMDrift]] - The problem being solved


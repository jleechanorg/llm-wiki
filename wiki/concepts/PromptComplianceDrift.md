---
title: "Prompt Compliance Drift"
type: concept
tags: [llm, prompt, compliance, drift, context-dilution]
sources: []
last_updated: 2026-04-11
---

## Description
LLM compliance drift occurs when the model ignores or partially follows critical instructions embedded in long prompts. The model produces outputs that violate stated rules — not due to capability limits, but due to prompt density and instruction placement.

## Symptoms
- **LLM emits zeroed units** on faction minigame enablement (should categorize from `army_data.forces`)
- **LLM omits `tool_requests`** despite explicit prompt requirement
- **LLM invents resources** (territory=50, citizens=2500) that don't exist in state
- **LLM ignores negation instructions** ("Do NOT output zeros" → outputs zeros)
- **LLM uses cached FP/ranking** despite prompt saying "NEVER use cached values"

## Root Causes

### Context Dilution
25K+ token prompts scatter critical rules throughout, causing the model to lose focus. Gemini Flash ignores rules that are not at the prompt start.

### Negation Confusion
Negative instructions ("Do NOT emit zeroed units", "FORBIDDEN") are less effective than affirmative validation checkpoints.

### Tool vs State Conflict
Prompts say "never use cached FP" but header templates extract from cached `game_state`. Mixed signals cause the model to pick whichever is easier.

### Missing Sequencing
No explicit order for: categorize units → infer resources → call tools. Model may skip steps.

## Solutions

### Gating Block at Prompt Start
Consolidate critical rules into a single GATING BLOCK at the start of the prompt (~2K tokens):
```
GATE:
1. Categorize forces from army_data (soldiers/spies/elites)
2. Infer resources from campaign state (not invented)
3. Calculate FP using faction_calculate_power tool
4. Emit state_updates with non-zero units
```

### Affirmative Checkpoints over Negations
Replace "Do NOT output zeros" with:
```
CHECK: Have all unit counts been derived from army_data.forces?
```

### VALID/INVALID Few-Shot Examples
Show side-by-side examples of correct vs incorrect outputs so the model has pattern matching.

### Explicit Phased Response Structure
Split into Phase A (state preparation) and Phase B (tool calls) with chain-of-thought ordering.

## Connections
- [[LLMDrift]] — related: consistency over long sequences
- [[Schema-PromptDrift]] — schema vs prompt alignment
- [[LLM-as-Judge-Pattern]] — self-validation checkpoints

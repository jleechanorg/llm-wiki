---
title: "Extended Reasoning & Test-Time Compute — Frontier AI (2026)"
type: source
tags: [extended-reasoning, test-time-compute, chain-of-thought, o3, o4, reasoning-models, self-critique, scaling-law]
date: 2026-04-14
source_file: frontier-research/extended-reasoning-2026.md
---

## Summary

The biggest AI coding shift in 2026: instead of making models bigger at training time, give them more inference-time compute to think longer, self-critique, revise, and explore multiple paths before outputting code. OpenAI o3/o4 and Anthropic extended thinking modes show extra thinking tokens often beat bigger models for complex coding tasks. This is the new scaling law.

## Key Claims

### The New Scaling Law: Test-Time Compute
- Old scaling: bigger model = better results (expensive at training time)
- New scaling: more thinking tokens at inference = better results (expensive at inference time)
- o3/o4 mode: model generates extended reasoning traces before responding
- Often beats a 10x larger model with one-shot response

### Why This Matters for Coding Agents
| Scenario | Without Extended Thinking | With Extended Thinking |
|----------|-------------------------|----------------------|
| Complex bug | One-shot fix attempt | Self-critique loop until fix verified |
| Architecture decision | Pick first option | Weigh tradeoffs, revise, self-verify |
| PR review | Single pass | Multi-pass critique with verification |
| Hard problem | Give up or guess | Think through edge cases, self-correct |

### Reasoning Budget Pattern
- Allocate N "thinking tokens" before final output
- Model self-critiques within the budget
- Budget can be adaptive: more for harder problems
- Your beads/evidence system provides the perfect feedback loop for this

### Connection to Your Setup
- [[HarnessEngineering]] — reasoning budget is a harness parameter
- [[SelfCritique]] — model critiques its own output within the reasoning budget
- [[ExtendedThinking]] — the specific mechanism (extended chain-of-thought)

## Connections

- [[ExtendedThinking]] — concept page
- [[ReasoningBudget]] — concept page
- [[SelfCritique]] — concept page
- [[MetaHarness]] — harness search could optimize reasoning budget allocation

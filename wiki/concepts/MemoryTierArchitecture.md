---
title: "Memory Tier Architecture"
type: concept
tags: [memory, project-memory, feedback-memory, outcome-ledger, compounding, openclaw]
last_updated: 2026-03-15
sources: [jleechanclaw-orchestration-system-design]
---

## Summary
The OpenClaw orchestration system uses three memory tiers that compound across every task. Without memory, every CI failure is the first CI failure the system has ever seen. With the outcome ledger, a `ModuleNotFoundError` on a Django project triggers a known-good fix strategy instead of random exploration.

## The Three Tiers

| Tier | What it stores | Used for |
|------|---------------|----------|
| **Project memories** | Codebase conventions, known patterns, historical decisions | Every LLM call gets context the agent earned from prior sessions |
| **Feedback memories** | Corrections and preferences from the developer | Shapes judgment — the agent learns what Jeffrey would have said |
| **Outcome ledger** | Which fix strategies succeeded or failed, indexed by error class | Future retries skip strategies that didn't work before |

## How Memory Flows

```
Agent session completes
  → outcome_recorder.record_outcome(error_class, strategy, result)
  → outcomes.jsonl: {error_class, strategy, success, timestamp}
  ↓
pattern_synthesizer.py (cron, nightly)
  → "for ImportError on Django models, strategy-B wins 78% of the time"
  ↓
generate_fix_strategies() seeds with known-winning strategies for next retry
```

## Project Memories

```
"In this repo, tests must be committed separately from implementation"
  → Stored in project memory during onboarding
  → Every new agent session gets this as context
  → Agents follow the convention without per-session re-instruction
```

## Feedback Memories

```
Developer: "stop marking PRs ready when CodeRabbit has open comments"
  → OpenClaw stores feedback memory
  → Future PR reviews: memory injected into review_pr() LLM context
  → OpenClaw applies the correction without being told again
```

## Why Memory Is the Prerequisite

A stateless agent is permanently dumb. Without the outcome ledger, the system burns retries on strategies that have never worked. Without the failure budget, it loops forever. Without escalation, the developer never finds out the loop is broken.

The memory system makes the "Replace Yourself" north star achievable — the system gets smarter over time instead of staying permanently dumb.

## Related Concepts
- [[AutonomousAgentLoop]]
- [[HarnessEngineering]]
- [[EscalationRouter]]
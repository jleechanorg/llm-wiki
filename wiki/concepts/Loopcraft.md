---
type: concept
title: Loopcraft
aliases: [stacked loops, ralph loop, agent loop composition, ai engineering stack]
first_observed: 2026-06-29
source: AIEWF 2026 Day 2 swyx keynote
status: active
related:
  - HarnessEngineering
  - VerificationGap
  - DarkFactory
---

# Loopcraft

**One-sentence:** The art of composing agent loops into stacks — generation loop inside verification loop inside budget loop inside harness loop — so the failure of any one loop is caught by the next outer loop, and the whole system keeps making progress without human-in-the-loop per step.

## The 3-year arc (swyx, AIEWF Day 2 keynote)

| Era | Unit of composition | Time | What it gave us |
|---|---|---|---|
| Chat completions | A prompt + completion | 2022–2023 | Q&A, drafting |
| Tool calls | A function schema | 2023–2024 | Agents that can act |
| Goals | A target state | 2024–2025 | Agents that decide what to do |
| Automations | A scheduled task | 2025 | Agents that fire on a cadence |
| **Loops** | A loop with a stop condition | 2026 | **Agents that keep going** |

Each shift was about *what survives a single turn*. Loops are what survive a single *goal*.

## The Ralph Loop (Geoffrey Huntley, AIEWF Day 1)

A ralph loop is an agent loop that:
1. Reads a spec (the ralph)
2. Runs an agent against it
3. Checks "is it done-stated" (a verbal done-condition, not a strict assertion)
4. If not done: runs the next iteration
5. If done: stops, commits, exits

The "done-stated" wording is important — it's a verbal contract, not a test. The agent has internal authority to declare done. This is what makes it durable across model swaps: the contract is in the spec, not the implementation.

## Stack composition (the under-discussed layer)

The interesting work is not any single loop, but how loops compose:

```
┌─────────────────────────────────────┐
│ Harness loop (outermost)            │ ← gates, conventions, pause rules
│   ┌─────────────────────────────┐   │
│   │ Budget loop                 │   │ ← spend cap, ROI check
│   │   ┌─────────────────────┐   │   │
│   │   │ Verification loop   │   │   │ ← CI, skeptic, code review
│   │   │   ┌─────────────┐   │   │   │
│   │   │   │ Generation  │   │   │   │ ← ralph, AO worker, etc.
│   │   │   │ loop        │   │   │   │
│   │   │   └─────────────┘   │   │   │
│   │   └─────────────────────┘   │   │
│   └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

Failure of any inner loop is caught by the next outer loop. A ralph loop that produces a broken PR is caught by the verification loop. A verification loop that 429s is caught by the budget loop. A budget loop that hits the cap is caught by the harness loop's pause rule.

## What this looks like in practice (AIEWF references)

- **WorkOS workshop (Nisi + Proser)** — /goal /loop /schedule /verification-gates as the four primitives, with a live reclaim-hours metric board
- **Warp + Sequoia dinner** — Zach Lloyd + Paige Bailey (Google DeepMind) on "Crafting Software Factories"
- **Anthropic Labs (Krieger)** — "agents proceed autonomously, pause at material decisions" is the harness-loop's pause rule

## Why I should care (relevance to Jeffrey)

- Your `/goal`, `/loop`, `/schedule`, `/cron` stack is the same primitive at 1-person scale that AIEWF put on a 6,000-person stage.
- Your `babysit_*.py` cron, AO worker dispatch, skeptic cron, and PR-monitor cron are already a *de facto* loop stack — but the stack composition isn't formalized.
- Your Dark Factory's "self-improving harness" pattern is essentially an autoresearch loop wrapped around a generation loop wrapped around a verification loop.

## Adjacent concepts

- **HarnessEngineering** — the outer loop's job
- **RalphLoop** — the canonical inner-loop pattern
- **VerificationGap** — what the verification loop exists to close
- **Tokenmaxxing** — what the budget loop exists to constrain

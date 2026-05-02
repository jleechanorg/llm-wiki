---
title: "Anthropic Harness Design for Long-Running Apps"
type: source
tags: [harness, multi-agent, generator-evaluator, context-reset, sprint-contract, anthropic]
date: 2026-03-24
source_file: https://www.anthropic.com/engineering/harness-design-long-running-apps
---

## Summary
Anthropic's engineering blog describes how multi-agent harness architectures dramatically improved Claude's performance on frontend design and autonomous software engineering. The key pattern is GAN-style generator-evaluator separation, context resets to combat "context anxiety," and sprint contracts negotiated before each build chunk. Results: 6hr/$200 harness vs 20min/$9 solo for a 2D retro game maker.

## Key Claims
- **Generator/Evaluator separation** produces skeptical external feedback vs lenient self-assessment — "Separating the agent doing the work from the agent judging it proves to be a strong lever"
- **Context resets** solve both context window filling and "context anxiety" (premature wrapping). Compaction alone doesn't give a clean slate.
- **Sprint contracts** bridge high-level specs to testable implementation criteria — one sprint had 27 test criteria
- **File-based handoffs** carry state between agents reliably across restarts
- **Three-agent architecture**: Planner (expands prompts into full specs) → Generator (one feature at a time) → Evaluator (tests via Playwright, grades against hard thresholds)
- Evaluator tuned via few-shot examples showing score drift; even tuned, agents miss subtle bugs in nested features
- Opus 4.6 largely eliminated context anxiety, allowing harness simplification

## Key Quotes
> "When asked to evaluate work they've produced, agents tend to respond by confidently praising the work — even when, to a human observer, the quality is obviously mediocre... Separating the agent doing the work from the agent judging it proves to be a strong lever to address this issue."

> "A reset provides a clean slate, at the cost of the handoff artifact having enough state for the next agent to pick up the work cleanly."

## Connections
- [[GeneratorEvaluatorSeparation]] — core pattern from this source
- [[ContextAnxiety]] — the problem context resets solve
- [[SprintContract]] — negotiated scope lock before build chunks
- [[FileBasedHandoffs]] — state persistence between agent restarts
- [[Harness5LayerModel]] — layered architecture this contributed to

## Key Implementation Details
- Four grading criteria: Design/Architecture (high weight), Originality (high weight), Craft (standard), Functionality (standard)
- Evaluator uses Playwright MCP for live page interaction and grading
- Sprint contract example: "Sprint 3: user auth. Done: (1) /login renders, (2) POST /api/login returns 200 JWT"
- Hard thresholds per criterion — any breach triggers detailed feedback
- Harness simplification with Opus 4.6: removed sprint construct, moved evaluator to single end-pass

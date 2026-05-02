---
title: "Generator Evaluator Separation"
type: concept
tags: [generator, evaluator, harness, quality-gate, GAN]
date: 2026-03-24
source: [[anthropic-harness-design-long-running-apps]]
---

## Definition
The pattern of separating the agent that **generates** work from a distinct agent that **evaluates** it. When the same agent does both, it grades its own output generously — evaluation becomes self-serving rather than independent.

## Why It Works
> "When asked to evaluate work they've produced, agents tend to respond by confidently praising the work — even when, to a human observer, the quality is obviously mediocre." — Anthropic

A generator/evaluator split produces skeptical external feedback. The evaluator is calibrated to be strict, not friendly. Few-shot examples with score drift align judgment.

## In the Autonomous Harness
- **Generator**: Implements sprint contract, self-evaluates before handoff
- **Evaluator**: AO skeptic agent (upgraded), tests via CanonicalCodeScorer rubric, emits dual verdict (EVIDENCE + QUALITY)

## Key Requirements
1. Evaluator must be tuned skeptical via few-shot calibration
2. Hard thresholds on grading criteria — any breach = fail
3. Evaluator never sees Generator's self-eval (prevents anchoring bias)
4. Generator and Evaluator are separate agent sessions

## Connections
- [[Harness5LayerModel]] — L4 verification layer
- [[CanonicalCodeScorer]] — the Evaluator's scoring engine
- [[SelfCritiqueVerificationLoop]] — Evaluator's inner iteration loop
- [[DualVerdict]] — EVIDENCE + QUALITY dual verdict architecture

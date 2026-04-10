---
title: "LLM Judgment"
type: concept
tags: ["llm", "judgment", "ai", "decision-making"]
sources: ["harness-engineering-philosophy"]
last_updated: 2026-04-07
---

LLM Judgment is the layer in harness engineering where an LLM (OpenClaw) makes decisions when deterministic reactions cannot handle the situation. This is the "outer loop" — called when the predictable 80% is exhausted.

## When LLM Judgment Is Used
- Vague review comments
- Task decomposition needed
- Conflicting failures
- Strategy decisions
- Retry with different strategy vs escalate to human

## Principle
"Deterministic first, LLM for judgment" — don't use an LLM when a rule will do. The LLM is called only for the 20% requiring genuine judgment.

## Related Concepts
- [[OpenClaw]] — provides LLM judgment capability
- [[Deterministic Feedback Loops]] — handles the predictable 80%
- [[Harness Engineering]] — overall framework

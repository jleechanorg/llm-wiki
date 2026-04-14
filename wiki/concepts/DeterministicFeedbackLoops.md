---
title: "Deterministic Feedback Loops"
type: concept
tags: [deterministic-feedback, automated-feedback, scripted-verification, LLM-automation, orchestration]
sources: [harness-engineering-philosophy]
last_updated: 2026-04-14
---

Deterministic feedback loops are the deterministic responses to predictable events provided by the agent-orchestrator. This is the "inner loop" — agent acts, CI/review state changes, AO reacts, agent acts again. They are also the low-cost, high-reliability feedback mechanism that complements expensive LLM-judged feedback.

## Examples
- CI failed → auto-send to agent, 2 retries
- Changes requested → auto-send to agent, escalate after 30m
- Agent stuck → notify, priority urgent

## Philosophy
This follows the Spotify Honk pattern: "reduced flexibility increases predictability." The LLM is called only when the deterministic router has no rule.

## Layer 2: Why This Matters as a Connection

Deterministic Feedback Loops were not previously linked to [[VerificationLoop]], [[ProcessRewardModel]], or [[SkepticGate]] — they were described only in the context of agent orchestration. As a Layer 2 discovery, they bridge agent-orchestration patterns (inner loop) with the verification pipeline (outer loop). In the [[VerificationLoop]], deterministic checks are the fast-fail stage before expensive LLM-judged loops. [[SkepticGate]] validates that deterministic feedback artifacts exist and are fresh.

## Layer 2 Connections

- [[VerificationLoop]] — deterministic feedback loops are the fast-fail stage before expensive LLM-judged loops in the verification pipeline
- [[ProcessRewardModel]] — PRM provides semi-deterministic step-level feedback (model-based but consistent)
- [[SkepticGate]] — SkepticGate validates that deterministic feedback artifacts exist and are fresh
- [[CI-Gates]] — deterministic checks are the implementation of fast-fail CI gate strategies
- [[LLM-as-Judge-Pattern]] — complements LLM-judged feedback: deterministic for fast/cheap checks, LLM-judged for semantic evaluation

## Related Concepts
- [[Agent Orchestrator]] — provides deterministic reactions
- [[LLM Judgment]] — called when deterministic routes exhaust
- [[Harness Engineering]] — overall discipline
- [[MetaHarness]] — Meta-Harness uses filesystem-based history to provide rich feedback (full code + traces + scores) rather than compressed summaries

## Examples
- CI failed → auto-send to agent, 2 retries
- Changes requested → auto-send to agent, escalate after 30m
- Agent stuck → notify, priority urgent

## Philosophy
This follows the Spotify Honk pattern: "reduced flexibility increases predictability." The LLM is called only when the deterministic router has no rule.

## Related Concepts
- [[Agent Orchestrator]] — provides these reactions
- [[LLM Judgment]] — called when deterministic routes exhaust
- [[Harness Engineering]] — overall discipline
- [[MetaHarness]] — Meta-Harness uses filesystem-based history to provide rich feedback (full code + traces + scores) rather than compressed summaries

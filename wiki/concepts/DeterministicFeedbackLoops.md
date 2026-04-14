---
title: "Deterministic Feedback Loops"
type: concept
tags: ["feedback", "deterministic", "orchestration", "automation"]
sources: ["harness-engineering-philosophy"]
last_updated: 2026-04-07
---

Deterministic feedback loops are the deterministic responses to predictable events provided by the agent-orchestrator. This is the "inner loop" — agent acts, CI/review state changes, AO reacts, agent acts again.

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

---
title: "Predictability-Adaptability Frontier"
type: concept
tags: ["orchestration", "tradeoff", "predictability", "adaptability"]
sources: ["orchestration-architecture-research"]
last_updated: 2026-04-07
---

Concept from Microsoft Agent Framework describing the fundamental trade-off in orchestration design:
- **Sequential pipeline** = predictable but not adaptive
- **Conversational multi-agent** = adaptive but less predictable

The orchestrator's design implements this trade-off by choosing when to use deterministic vs LLM-driven approaches.

## See Also
- [[Microsoft]]
- [[Hybrid Orchestration]]
- [[LLM-Driven Orchestration]]
- [[Deterministic Orchestration]]
- [[Orchestration Architecture Research]]

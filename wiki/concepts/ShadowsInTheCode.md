---
title: "ShadowsInTheCode"
type: concept
tags: [security, multi-agent, ChatDev, MetaGPT, AgentVerse]
sources: [shadows-in-code-paper]
last_updated: 2026-04-14
---

Security vulnerabilities in LLM multi-agent development systems. IMBIA attack embeds hidden malicious functionality in multi-agent pipelines. AAAI 2026.

## Two Threat Scenarios

1. **MU-BA**: Malicious User exploits Benign Agent
2. **BU-MA**: Benign User exposed to compromised Agent (MA)

## Attack Rates

| Framework | MU-BA | BU-MA |
|-----------|-------|-------|
| ChatDev | 93% | 71% |
| MetaGPT | 45% | 84% |
| AgentVerse | 71% | 45% |

## Key Insight

Agents in **coding and testing phases** pose the highest security risk — they have the most access to modify code.

## Connections

- Related to [[MetaGPT]] — same frameworks studied
- [[VibeCodingSafe]] — security implications of agent adoption
- [[ZeroFrameworkCognition]] — safety considerations

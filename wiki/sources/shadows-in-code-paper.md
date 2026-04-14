---
title: "Shadows in the Code: Security Risks in LLM-Based Multi-Agent Development Systems"
type: source
tags: [security, multi-agent, ChatDev, MetaGPT, AgentVerse, AAAI-2026]
sources: []
date: 2025-11-23
source_file: raw/arxiv-2511.18467-shadows-in-code.md
---

## Summary

Identifies novel security vulnerabilities in LLM multi-agent development. IMBIA attack embeds hidden malicious functionality. Tested on ChatDev, MetaGPT, AgentVerse. MU-BA attack rates up to 93%, BU-MA up to 84%.

## Key Claims

- Two threat scenarios: **MU-BA** (malicious user exploits benign agent) and **BU-MA** (benign user exposed to compromised agent)
- Agents in coding and testing phases pose highest security risk
- **IMBIA** attack manipulates multi-agent pipelines

## Attack Results

| Framework | MU-BA Attack Rate | BU-MA Attack Rate |
|-----------|-------------------|-------------------|
| ChatDev | 93% | 71% |
| MetaGPT | 45% | 84% |
| AgentVerse | 71% | 45% |

## Connections

- Related to [[MetaGPT]] — multi-agent vulnerabilities
- Related to [[VibeCodingSafe]] — security implications
- [[ZeroFrameworkCognition]] — safety considerations

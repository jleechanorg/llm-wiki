---
title: "MetaGPT"
type: concept
tags: [multi-agent, coding-agent, SOPs, role-assignment, meta-programming]
sources: [metagpt-paper]
last_updated: 2026-04-14
---

Multi-agent framework incorporating Standardized Operating Procedures (SOPs) into LLM collaborations. Assembly-line paradigm assigns diverse roles to agents who work together on complex software engineering tasks.

## Core Insight

> "SOPs inject human-like domain expertise into agent workflows"

## Architecture Pattern

```
SOP Encoded as Prompts
        ↓
Role Assignment: [Architect | Engineer | Tester | ...]
        ↓
Intermediate Verification Gates
        ↓
Structured Output Artifacts
```

## Key Claims

- Addresses cascading hallucinations in naive LLM chaining
- Agents verify intermediate results against expected artifacts
- Structured outputs (design docs, code, tests) reduce free-form drift

## Connections

- Related to [[Voyager]] — structured collaboration vs. single-agent iteration
- Related to [[Multi-Agent Coordination]] concepts
- [[AgentMentor]] extends verification into corrective instruction loops

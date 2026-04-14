---
title: "SWE-Agent"
type: concept
tags: [coding-agent, SWE-bench, agentic, software-repair]
sources: [swe-agent-paper]
last_updated: 2026-04-14
---

Autonomous software engineering agent using LLMs to resolve issues in real GitHub repositories. Introduces the Agent Computer Interface (ACI) — structured interface between LLM and development tools for efficient, reliable software engineering.

## Agent Computer Interface (ACI)

Key insight: proper tooling design dramatically improves LLM effectiveness for SE tasks.

Core principles:
- **Specialized tool definitions** for git, code search, file editing
- **Iterative refinement** through feedback from tool outputs
- **Repository context management** for handling large codebases

## Connections

- Related to [[OpenHands]] — open platform for coding agents
- Related to [[SWE-Shepherd]] — PRM-based step-level guidance
- Related to [[SWE-bench]] — benchmark for software engineering

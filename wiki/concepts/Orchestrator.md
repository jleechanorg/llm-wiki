---
title: "Orchestrator"
type: concept
tags: [system-design, agent-coordination, benchmark]
sources: []
last_updated: 2026-04-07
---

An orchestrator is a system that coordinates multiple AI agents to execute complex software development tasks. The benchmark compared two orchestrators: [[Genesis]] and [[Ralph]].

## Key Components
- **Agent Management**: Mapping and execution of AI agents (Codex, Claude)
- **Execution Models**: tmux sessions vs background processes
- **Monitoring**: Session tracking vs process ID logging

## Benchmark Findings
- Both systems achieved high success rates (83-100%)
- Execution model differences affect observability and recoverability
- Agent adapter configuration is critical for consistency

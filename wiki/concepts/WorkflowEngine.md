---
title: "Workflow Engine"
type: concept
tags: [workflow, orchestration, yaml, durable-execution, dag]
date: 2026-04-15
---

## Overview

A workflow engine orchestrates multi-step processes, often encoded as YAML DAGs, DOT graphs, or code-first workflows. For AI agents, workflow engines provide repeatability, isolation, and composability for agentic tasks.

## Key Properties

- **YAML/DOT workflow DAGs**: Declarative agent task definitions
- **Durable execution**: Crash-proof workflow state persistence
- **Event sourcing**: History-based workflow replay
- **Activity retries**: Automatic retry policies for failure-prone tasks
- **Git worktree isolation**: Each run in isolated parallel environment

## Key Systems

| System | Type | Key Distinction |
|--------|------|----------------|
| [[Archon]] | YAML DAGs | mission.md governance, git worktree isolation |
| [[Kilroy]] | DOT graphs | CXDB checkpoints, English-to-DOT ingestion |
| [[Mammoth]] | DOT graphs | 21-rule linter, fan-in, verification nodes |
| [[Tracker]] | Dippin language | .dipx bundles, interview-mode human gates |
| [[Temporal]] | Durable execution | Event sourcing, crash recovery |
| [[Prefect]] | Python-first | Single decorator turns functions into workflows |
| [[Airbyte]] | Data integration | MCP Server for agent data access |

## Attractor Pattern Implementations

Four independent Attractor implementations (Kilroy, Mammoth, Smasher, Tracker) converge on the same three-layer workflow engine architecture:
1. **Unified LLM Client** — provider adapters
2. **Agent Loop** — tool dispatch, steering, subagents
3. **Pipeline Engine** — DOT parser, graph walker, node handlers, checkpointing

## Workflow Engine vs Governance

Workflow engines define *how* tasks run. Governance layers define *what* constraints apply. Archon conflates the two (governance is consulted on every decision). AO's proposed governance layer keeps them separate.

## See Also
- [[Archon]]
- [[Kilroy]]
- [[Mammoth]]
- [[Tracker]]
- [[Temporal]]
- [[Prefect]]
- [[Airbyte]]
- [[DurableExecution]]
- [[AttractorPattern]]

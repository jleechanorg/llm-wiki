---
title: "Workflow Engine"
type: concept
tags: [workflow, orchestration, yaml, durable-execution, dag]
date: 2026-04-15
---

## Overview

A workflow engine orchestrates multi-step processes, often encoded as YAML DAGs or code-first workflows. For AI agents, workflow engines provide repeatability, isolation, and composability for agentic tasks.

## Key Properties

- **YAML workflow DAGs**: Declarative agent task definitions
- **Durable execution**: Crash-proof workflow state persistence
- **Event sourcing**: History-based workflow replay
- **Activity retries**: Automatic retry policies for failure-prone tasks
- **Git worktree isolation**: Each run in isolated parallel environment

## Key Systems

| System | Type | Key Distinction |
|--------|------|----------------|
| [[Archon]] | YAML DAGs | mission.md governance, git worktree isolation |
| [[Temporal]] | Durable execution | Event sourcing, crash recovery |
| [[Prefect]] | Python-first | Single decorator turns functions into workflows |
| [[Airbyte]] | Data integration | MCP Server for agent data access |

## Workflow Engine vs Governance

Workflow engines define *how* tasks run. Governance layers define *what* constraints apply. Archon conflates the two (governance is consulted on every decision). AO's proposed governance layer keeps them separate.

## See Also
- [[Archon]]
- [[Temporal]]
- [[Prefect]]
- [[Airbyte]]
- [[DurableExecution]]

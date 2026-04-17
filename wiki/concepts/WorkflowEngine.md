---
title: "Workflow Engine"
type: concept
<<<<<<< HEAD
tags: [architecture, ai-coding, yaml, dag]
=======
tags: [workflow, orchestration, yaml, durable-execution, dag]
>>>>>>> origin/fix/br-4bk-green-gate-design-doc-v2
date: 2026-04-15
---

## Overview

<<<<<<< HEAD
A workflow engine wraps AI coding sessions with structured DAG (Directed Acyclic Graph) definitions to make output deterministic and repeatable. Instead of hoping an AI does the right thing each time, the workflow defines: plan → implement → validate → review → PR.

## Archon as Archetype

Archon (coleam00/Archon) is the canonical example:
- YAML-defined workflows
- Wraps Claude Code SDK and OpenAI Codex SDK
- 17 built-in opinionated templates
- 2,781-line executor

## Key Pattern: Opinionated Templates

Archon's killer feature is automatic workflow routing:
- User: "I want to fix this bug"
- Archon: routes to `archon-fix-github-issue` workflow automatically

This requires buy-in to the abstraction but dramatically improves user adoption.

## Comparison with Orchestration

| Workflow Engine | Fleet Orchestrator |
|---|---|
| One AI session per workflow | Many AI agents in parallel |
| YAML-defined DAG steps | Event-driven reactions |
| Human kicks off | Autonomous detection and reaction |
| Deterministic within session | Non-deterministic across fleet |

## What AO Could Learn from Workflow Engines

1. **YAML workflow templates as first-class artifacts** — encode common reaction patterns as composable workflow YAML files
2. **Deterministic validation nodes** — explicit `bash: bun run validate` steps as model
3. **Command library structure** — 20+ `.archon/commands/defaults/` files as prompt templates
4. **Human-gate patterns** — `loop: until: ALL_TASKS_COMPLETE` combined with explicit approval nodes

See [[Archon]], [[jleechanorg/agent-orchestrator]], [[DarkFactory]], [[slack-c09grlxf9gr-archon-analysis-2026-04-15]].
=======
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
>>>>>>> origin/fix/br-4bk-green-gate-design-doc-v2

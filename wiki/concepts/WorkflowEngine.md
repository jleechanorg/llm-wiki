---
title: "Workflow Engine"
type: concept
tags: [architecture, ai-coding, yaml, dag]
date: 2026-04-15
---

## Overview

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

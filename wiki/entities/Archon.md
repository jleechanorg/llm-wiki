---
title: "Archon"
type: entity
tags: [workflow-engine, yaml-dag, autonomous-coding, dark-factory]
date: 2026-04-15
---

## Overview

Archon (coleam00/Archon) is a workflow engine for AI coding — "What Dockerfiles did for infrastructure and GitHub Actions did for CI/CD, Archon does for AI coding workflows." It makes AI coding deterministic and repeatable via YAML workflows.

## Key Properties

- **Creator**: Cole (coleam00)
- **Description**: "What Dockerfiles did for infrastructure and GitHub Actions did for CI/CD — Archon does for AI coding workflows"
- **Architecture layers**:
  - Platform Adapters (Web UI, CLI, Telegram, Slack, Discord, GitHub)
  - Orchestrator (message routing, context management)
  - Workflow Executor (YAML DAGs)
  - AI Assistant Clients (Claude/Codex)
  - SQLite/PostgreSQL persistence
- **Key features**: Repeatable, Isolated (git worktrees), Composable, Portable
- **Node types**: Prompt nodes (AI), Bash nodes (deterministic), Loop nodes, Interactive nodes
- **17 default workflows**: bug fix, feature development, PR review, conflict resolution, architecture sweeps
- **Governance**: DarkFactory pattern — mission.md + factory-rules.md consulted on every decision

## Connections

- [[DarkFactory]] — Archon uses DarkFactory governance pattern (mission.md + factory-rules.md)
- [[WorkflowEngine]] — Archon encodes workflows as YAML DAGs
- [[GovernanceLayer]] — Archon's governance is coupled (consulted on every decision) vs AO's decoupled constraint model
- [[YAMLWorkflow]] — Archon's YAML workflow definition pattern
- [[GitWorktreeIsolation]] — Archon uses git worktrees for run isolation

## See Also
- [[DarkFactory]]
- [[WorkflowEngine]]
- [[GovernanceLayer]]

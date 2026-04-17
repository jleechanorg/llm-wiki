---
title: "Archon"
type: entity
<<<<<<< HEAD
tags: [workflow-engine, ai-coding, typescript, bun]
=======
tags: [workflow-engine, yaml-dag, autonomous-coding, dark-factory]
>>>>>>> origin/fix/br-4bk-green-gate-design-doc-v2
date: 2026-04-15
---

## Overview

<<<<<<< HEAD
Archon (https://github.com/coleam00/Archon) is a TypeScript/Bun monorepo workflow engine for AI coding agents. It wraps Claude Code SDK and OpenAI Codex SDK with YAML-defined DAG workflows to make AI-assisted development deterministic and repeatable.

## Key Characteristics

- **Tech stack**: TypeScript monorepo, Bun runtime, v0.3.6
- **Stars**: ~18K GitHub stars
- **Active period**: Feb 2025–present, single developer
- **Core thesis**: Raw AI agent output is non-deterministic; Archon makes one agent's work deterministic via YAML workflows

## Architecture

Archon defines development lifecycle as YAML: plan → implement → validate → review → PR. The AI fills in the steps within a controlled DAG structure.

## Maturity Assessment

| Dimension | Score | Notes |
|---|---|---|
| Concept | 9/10 | Right idea; deterministic dev process |
| Architecture | 8/10 | Clean separation, good interfaces |
| Implementation | 7/10 | Solid but complex; 2,781-line executor |
| Maturity | 5/10 | v0.3.6, single developer, schema churn |
| Usability | 5/10 | YAML DSL; Bun-native, no npm/pnpm |

## Built-in Workflow Templates

17 opinionated templates including:
- `archon-fix-github-issue`
- `archon-idea-to-pr`
- `archon-plan-to-pr`

These are considered Archon's killer feature for user adoption.

## Dark Factory

Cole's "dark factory" is a speculative layer on Archon implementing governance-heavy autonomous issue processing:
- 3-worktree pipeline: triage → implementation → validation
- `mission.md` + `factory-rules.md` as governance constraints
- Human monitors and restarts; not truly zero-touch

## vs Agent-Orchestrator

Archon = workflow engine for **one** AI coding session per worktree.
AO fork = fleet orchestrator for **many** AI agents in parallel across PRs.

See [[slack-c09grlxf9gr-archon-analysis-2026-04-15]] for full comparison.
=======
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
>>>>>>> origin/fix/br-4bk-green-gate-design-doc-v2

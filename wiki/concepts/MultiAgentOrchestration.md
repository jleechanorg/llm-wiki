---
title: "Multi-Agent Orchestration"
type: concept
tags: [architecture, fleet, coordination, event-driven]
date: 2026-04-15
---

## Overview

Multi-agent orchestration coordinates many AI agents in parallel across multiple worktrees, PR lifecycles, or event streams. Unlike a workflow engine (which wraps one session), orchestration manages a fleet of sessions that respond to events autonomously.

## Agent-Orchestrator Fork as Archetype

| Component | Role |
|---|---|
| Event Bus | webhook-ingress, poller-GH-PR, MCP mail |
| Reaction Handlers | ci-failed, changes-requested, agent-stuck, stuck-worker-detector |
| Spawn Queue | tmux process runtime, git worktree per run |
| Agent Pool | Claude/Codex/Cursor/Gemini |
| Skeptic Gate | Independent LLM verification |
| Evidence Gate | 7-gate merge criteria |

## Evolve Loop

AO has an 8-phase autonomous loop:
- **OBSERVE** → **MEASURE** → **DIAGNOSE** → **PLAN** → **FIX** → **GROOM** → **COMMIT** → **REVIEW**
- Reads `GOVERNANCE.md` and `SCOPE.md` at startup as constraints
- Zero-touch target: 6 hours

## vs Workflow Engine

| Dimension | Multi-Agent Orchestration | Workflow Engine |
|---|---|---|
| Unit of work | N parallel sessions, each PR lifecycle | One workflow, one worktree |
| Who drives | Polls, detects events, reacts autonomously | Human says "do this feature" |
| Loop mode | Autonomous 8-phase loop | YAML until: ALL_TASKS_COMPLETE |
| Failure recovery | Explicit: stuck-worker-detector, parallel-retry | Implicit retry hooks |
| Verification | Skeptic independent LLM | Holdout validation pattern |

## Complementary Use

Archon's per-session workflow engine could contribute to AO at the **per-session execution level**. AO's YAML workflow approach (opinionated templates) could make `ao spawn` more accessible.

See [[jleechanorg/agent-orchestrator]], [[Archon]], [[WorkflowEngine]], [[slack-c09grlxf9gr-archon-analysis-2026-04-15]].

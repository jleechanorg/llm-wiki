---
title: "Multi-Agent Orchestration"
type: concept
<<<<<<< HEAD
tags: [architecture, fleet, coordination, event-driven]
=======
tags: [multi-agent, orchestration, coordination, fleet, workflow]
>>>>>>> origin/fix/br-4bk-green-gate-design-doc-v2
date: 2026-04-15
---

## Overview

<<<<<<< HEAD
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
=======
Multi-agent orchestration refers to frameworks and platforms that coordinate multiple AI agents working together on tasks. These systems contrast with single-agent systems by managing inter-agent communication, role assignment, and collective decision-making.

## Key Patterns

- **State machine orchestration**: Graph-based workflows with nodes and edges (LangGraph)
- **Group chat patterns**: Multiple agents communicating in shared context
- **Two-agent chats**: Simplified bilateral conversation patterns (AutoGen)
- **Human-in-the-loop**: Interactive approval gates in agent workflows
- **Event-driven message passing**: Core architecture for distributed agents
- **SOP encoding**: Standardized Operating Procedures as prompt sequences (MetaGPT)

## Key Frameworks

| Framework | Type | Key Feature |
|-----------|------|-------------|
| [[LangGraph]] | Framework | Graph-based state machines |
| [[AutoGen]] | Framework | Two-agent/group chats |
| [[CrewAI]] | Platform | Enterprise crew orchestration |
| [[MetaGPT]] | Framework | SOP-encoding assembly line |
| [[Microsoft Copilot Studio]] | Platform | Enterprise copilots |
| [[Microsoft Agent Framework]] | Framework | AutoGen successor |
| [[AgentBench]] | Benchmark | Multi-domain LLM evaluation |

## Relation to AO

AO's evolve loop is a single-agent 8-phase loop, not a multi-agent orchestration system. Governance layer proposals (PR #452/#453) do not add multi-agent coordination — they add governance constraints to AO's existing loop. Compare to:
- [[Archon]] which uses YAML DAGs for multi-workflow orchestration
- [[Temporal]] which uses durable execution for workflow state

## See Also
- [[LangGraph]]
- [[AutoGen]]
- [[CrewAI]]
- [[MetaGPT]]
- [[WorkflowEngine]]
>>>>>>> origin/fix/br-4bk-green-gate-design-doc-v2

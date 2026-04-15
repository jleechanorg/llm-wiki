---
title: "Multi-Agent Orchestration"
type: concept
tags: [multi-agent, orchestration, coordination, fleet, workflow]
date: 2026-04-15
---

## Overview

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

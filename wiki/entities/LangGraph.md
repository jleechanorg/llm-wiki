---
title: "LangGraph"
type: entity
tags: [multi-agent, orchestration, workflow, langchain, state-machine]
date: 2026-04-15
---

## Overview

LangGraph is a framework for building reliable agents with low-level control, built on top of LangChain. It models agent workflows as graph-based state machines where nodes represent agent states and edges represent transitions.

## Key Properties

- **Architecture**: Graph-based state machines for agent orchestration
- **Key feature**: Human-in-the-loop patterns via state management
- **Purpose**: Build reliable agents with low-level control over agentic workflows
- **Relation to LangChain**: Part of LangChain ecosystem; LangGraph adds cycle support and persistence

## Connections

- [[MultiAgentOrchestration]] — LangGraph is a multi-agent orchestration framework
- [[WorkflowEngine]] — LangGraph encodes workflows as directed graphs
- [[LangChain]] — parent project
- [[AutoGen]] — alternative multi-agent framework (Microsoft)

## See Also
- [[MultiAgentOrchestration]]
- [[WorkflowEngine]]

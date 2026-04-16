---
title: "Durable Execution"
type: concept
tags: [durability, fault-tolerance, event-sourcing, crash-recovery, temporal]
date: 2026-04-15
---

## Overview

Durable execution is a programming model where application state survives crashes, restarts, and failures. The system persists full execution state and can replay it from any checkpoint.

## Key Properties

- **Workflows**: Fault-tolerant, recoverable, replayable business logic as code
- **Activities**: Automatic retries for failure-prone logic (API calls, network ops)
- **Event sourcing**: Maintains detailed execution history for crash recovery
- **Replays**: Workflows can be replayed from any failure point

## Temporal Model

[[Temporal]] is the canonical implementation:
- **Workflows**: Business logic as code with durable state
- **Activities**: Functions with automatic retry policies
- **Temporal Service**: Persists application state with built-in retries, task queues, signals, and timers
- **SDKs**: Python, Go, TypeScript, Java, C#, Ruby, PHP

## AI Agent Applications

Durable execution is relevant for:
- Long-running AI agent tasks that must survive crashes
- Agentic workflows with multiple steps and state
- Training pipelines that must recover from partial failures

## See Also
- [[Temporal]]
- [[WorkflowEngine]]

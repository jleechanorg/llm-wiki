---
title: "Event Sourcing for Agents"
type: concept
tags: [attractor-pattern, event-sourcing, durable-execution, replay]
date: 2026-05-24
---
## Overview
Event sourcing for agents applies the event sourcing pattern (storing every state change as an immutable event) to agent pipeline execution. CXDB is the canonical implementation: every step is an event, enabling full replay, failure clustering, and checkpoint recovery.

## Key Properties
- **What**: Recording every agent pipeline step as an immutable event for replay, diagnosis, and recovery
- **Why matters**: Enables (1) resume from any checkpoint, (2) Healer-style failure clustering by (node, outcome, output_hash), (3) full audit trail for the dark factory
- **Key pattern**: Append-only event log → sequence counter independent of step count → WAL mode for concurrent writes
- **Distinction from traditional event sourcing**: Agent events include LLM I/O, tool calls, token counts, cost data — not just state transitions

## Related Systems
| System | Type | Relevance |
|--------|------|-----------|
| [[CXDB]] | Database | The canonical agent event sourcing implementation |
| [[DurableExecution]] | Concept | Temporal's event sourcing model for workflow state |
| [[HealerAgent]] | Agent | Reads event-sourced CXDB data to cluster failures |
| [[Temporal]] | System | Traditional event sourcing for durable workflows |

## Connection to Attractor Pattern
Event sourcing (via CXDB) is what makes the Attractor pattern's Healer possible. Without a complete event history, you can't cluster failures, diagnose root causes, or resume interrupted runs — all essential for autonomous dark factory operation.

## See Also
- [[CXDB]]
- [[DurableExecution]]
- [[HealerAgent]]

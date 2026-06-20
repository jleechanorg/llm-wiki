---
title: "WorldArchitect.AI Architecture — Agent Orchestration Patterns"
type: synthesis
tags: [worldarchitect-ai, agent-orchestration, ao, architecture, mctrl]
sources: [concepts/AgentOrchestrator, concepts/AgentRouting, concepts/AO-Blocker-Matrix, concepts/AgentStallRecovery, concepts/AO-Daemon-Incident]
last_updated: 2026-04-14
---

## Summary

WorldArchitect.AI uses a multi-agent orchestration architecture with Claude Code, Codex, and Gemini integrated via agent adapters. The system handles TTRPG campaign management, dice authenticity, streaming LLM responses, and autonomous task execution. Key architectural patterns include: priority-based agent routing, stall recovery with watchdog timers, evidence-based PR quality gates, and split-brain detection for multi-client coordination.

## Key Insights

### 1. Agent Orchestrator Core Architecture

[AgentOrchestrator](../entities/AgentOrchestrator.md) coordinates multiple AI agents:
- **Claude Code** (primary CLI agent)
- **Codex** (secondary code agent)
- **Gemini** (research/analysis)
- **mctrl** (lifecycle/mail integration)

The [AgentAdapter](../concepts/AgentAdapter.md) provides a unified interface across different agent implementations. [AgentArchitecture](../concepts/AgentArchitecture.md) defines the class hierarchy: agents receive tasks, classify intent, route to appropriate handler, emit structured responses.

### 2. Agent Routing and Priority

[AgentRouting](../concepts/AgentRouting.md) and [AgentSelection](../concepts/AgentSelection.md) handle task distribution:
- [AgentPriorityOrdering](../concepts/AgentPriorityOrdering.md) assigns urgency/importance scores
- [AgentModeDetection](../concepts/AgentModeDetection.md) identifies agent state (idle, working, waiting_for_input)
- Routing uses [FastEmbed](../entities/FastEmbed.md) semantic intent classification
- Fallback chains: primary → secondary → human escalation

### 3. Stall Recovery and Watchdog Patterns

[AgentStallRecovery](../concepts/AgentStallRecovery.md) implements watchdog timers:
- Timeout detection per agent task
- Recovery strategies: retry, escalate, handoff
- [AO-Daemon-Incident](../concepts/AO-Daemon-Incident.md) documents a WebSocket streaming incident where the daemon failed to detect a stalled agent, requiring manual restart

### 4. Blocker Matrix for PR Quality Gates

[AO-Blocker-Matrix](../concepts/AO-Blocker-Matrix.md) tracks 7-green criteria for PRs:
1. CI passes
2. Mergeable state clean
3. Code review approved
4. Bugbot clean
5. Inline comments resolved
6. Evidence review passes
7. Skeptic passes

The [HarnessEngineering](../concepts/HarnessEngineering.md) page documents harness failure patterns — CI/skeptic/evidence gates that fail non-deterministically.

### 5. Streaming and Error Handling

[ErrorHandlingInStreaming](../concepts/ErrorHandlingInStreaming.md) and [AsyncioOrchestrationMigration](../concepts/AsyncioOrchestrationMigration.md):
- Streaming LLM responses require async handling
- [Hybrid-Orchestration](../concepts/Hybrid-Orchestration.md) combines synchronous (CLI) and asynchronous (streaming) paths
- [Deterministic-Orchestration](../concepts/Deterministic-Orchestration.md) provides reproducible runs for testing

The [StreamingParity](../concepts/StreamingParity.md) issue (same pattern as Level-Up Bug): streaming path bypasses postcondition enforcement that non-streaming path runs.

### 6. Split-Brain Detection

[AO-Split-Brain](../concepts/AO-Split-Brain.md) and [AO-Uncovered-Split](../concepts/AO-Uncovered-Split.md):
- Occurs when multi-client coordination fails
- Daemon thinks agent is running, agent thinks it's waiting
- Detection via heartbeat/ack timeout
- Recovery: force reconnect, state reconciliation

### 7. Evidence-Based Verification

The [EvidenceReviewPipeline](../concepts/EvidenceReviewPipeline.md) (two-stage pipeline):
- **Stage 1:** Automated checks (sha256 verification, scope validation)
- **Stage 2:** Skeptic review (claims classification, proof requirements)
- Evidence publication rule: committing to git ≠ published; must add gist/evidence URL to PR description

## Connections

- [AgentOrchestrator](../entities/AgentOrchestrator.md) — core coordinator
- [AgentAdapter](../concepts/AgentAdapter.md) — unified interface
- [AgentRouting](../concepts/AgentRouting.md) — priority-based routing
- [AgentStallRecovery](../concepts/AgentStallRecovery.md) — watchdog timers
- [AO-Blocker-Matrix](../concepts/AO-Blocker-Matrix.md) — 7-green PR criteria
- [AO-Daemon-Incident](../concepts/AO-Daemon-Incident.md) — WebSocket streaming failure
- [StreamingParity](../concepts/StreamingParity.md) — streaming vs non-streaming divergence
- [EvidenceReviewPipeline](../concepts/EvidenceReviewPipeline.md) — two-stage verification
- [AsyncioOrchestrationMigration](../concepts/AsyncioOrchestrationMigration.md) — async coordination

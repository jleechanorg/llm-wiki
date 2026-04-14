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

[[AgentOrchestrator]] coordinates multiple AI agents:
- **Claude Code** (primary CLI agent)
- **Codex** (secondary code agent)
- **Gemini** (research/analysis)
- **mctrl** (lifecycle/mail integration)

The [[AgentAdapter]] provides a unified interface across different agent implementations. [[AgentArchitecture]] defines the class hierarchy: agents receive tasks, classify intent, route to appropriate handler, emit structured responses.

### 2. Agent Routing and Priority

[[AgentRouting]] and [[AgentSelection]] handle task distribution:
- [[AgentPriorityOrdering]] assigns urgency/importance scores
- [[AgentModeDetection]] identifies agent state (idle, working, waiting_for_input)
- Routing uses [[FastEmbed]] semantic intent classification
- Fallback chains: primary → secondary → human escalation

### 3. Stall Recovery and Watchdog Patterns

[[AgentStallRecovery]] implements watchdog timers:
- Timeout detection per agent task
- Recovery strategies: retry, escalate, handoff
- [[AO-Daemon-Incident]] documents a WebSocket streaming incident where the daemon failed to detect a stalled agent, requiring manual restart

### 4. Blocker Matrix for PR Quality Gates

[[AO-Blocker-Matrix]] tracks 7-green criteria for PRs:
1. CI passes
2. Mergeable state clean
3. Code review approved
4. Bugbot clean
5. Inline comments resolved
6. Evidence review passes
7. Skeptic passes

The [[HarnessEngineering]] page documents harness failure patterns — CI/skeptic/evidence gates that fail non-deterministically.

### 5. Streaming and Error Handling

[[ErrorHandlingInStreaming]] and [[AsyncioOrchestrationMigration]]:
- Streaming LLM responses require async handling
- [[Hybrid-Orchestration]] combines synchronous (CLI) and asynchronous (streaming) paths
- [[Deterministic-Orchestration]] provides reproducible runs for testing

The [[StreamingParity]] issue (same pattern as Level-Up Bug): streaming path bypasses postcondition enforcement that non-streaming path runs.

### 6. Split-Brain Detection

[[AO-Split-Brain]] and [[AO-Uncovered-Split]]:
- Occurs when multi-client coordination fails
- Daemon thinks agent is running, agent thinks it's waiting
- Detection via heartbeat/ack timeout
- Recovery: force reconnect, state reconciliation

### 7. Evidence-Based Verification

The [[EvidenceReviewPipeline]] (two-stage pipeline):
- **Stage 1:** Automated checks (sha256 verification, scope validation)
- **Stage 2:** Skeptic review (claims classification, proof requirements)
- Evidence publication rule: committing to git ≠ published; must add gist/evidence URL to PR description

## Connections

- [[AgentOrchestrator]] — core coordinator
- [[AgentAdapter]] — unified interface
- [[AgentRouting]] — priority-based routing
- [[AgentStallRecovery]] — watchdog timers
- [[AO-Blocker-Matrix]] — 7-green PR criteria
- [[AO-Daemon-Incident]] — WebSocket streaming failure
- [[StreamingParity]] — streaming vs non-streaming divergence
- [[EvidenceReviewPipeline]] — two-stage verification
- [[AsyncioOrchestrationMigration]] — async coordination

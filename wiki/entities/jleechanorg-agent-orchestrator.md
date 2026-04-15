---
title: "jleechanorg/agent-orchestrator"
type: entity
tags: [multi-agent, orchestration, fleet-orchestrator, typescript]
date: 2026-04-15
---

## Overview

The jleechanorg/agent-orchestrator fork is a multi-agent fleet orchestration system that coordinates many AI agents in parallel across PR lifecycles. It is NOT a workflow engine — it is a coordination layer.

## Key Architecture

| Component | Role |
|---|---|
| Event Bus | webhook-ingress, poller-GH-PR, MCP mail |
| Reaction Handlers | ci-failed, changes-requested, agent-stuck, stuck-worker-detector, stalled-worker-auditor |
| Spawn Queue | Session manager with tmux process runtime |
| Skeptic Gate | Independent LLM verification (not GHA API keys) |
| Evidence Gate | 7-gate merge criteria |
| Agent Pool | Claude/Codex/Cursor/Gemini |
| GitHub PR/CR | Merge coordination |

## Evolve Loop (eloop)

AO has a built-in 8-phase autonomous loop:
1. **OBSERVE** — capture tmux panes, check PRs, detect cold PRs and stuck workers
2. **MEASURE** — zero-touch rate calculation, worker health, reaction failure rate
3. **DIAGNOSE** — classify anomalies, check bead tracker, dedup via JSONL KB
4. **PLAN** — P0/P1/P2 triage
5. **FIX** — autonomous disambiguation
6. **GROOM** — PR preparation
7. **COMMIT** — git operations
8. **REVIEW** — CR analysis

The loop reads `GOVERNANCE.md` and `SCOPE.md` at startup and injects them as constraints in Phase 1.

## Governance

- `agent-orchestrator.yaml` controls behavior via agentRules and reactions
- Skeptic verdict and evidence bundle written as markdown artifacts for human audit
- IMPLICIT_DENY_LIST as hard constraints
- Unlike Archon, governance runs periodically rather than on every decision

## vs Archon

AO coordinates **many** parallel agents across **many** PRs/events.
Archon wraps **one** agent session with YAML DAGs.

The two are complementary: Archon's per-session workflow engine could contribute to AO at the execution level.

## Maturity

Production-minded level 4 system with level 5 (zero-touch) aspirations. Skeptic is deployed and running. Evolve loop is built-in.

See [[slack-c09grlxf9gr-archon-analysis-2026-04-15]] for full comparison.

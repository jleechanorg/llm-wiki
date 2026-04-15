---
title: "Governance Layer"
type: concept
tags: [governance, constraints, ai-safety, policy]
date: 2026-04-15
---

## Overview

A governance layer encodes what an AI system should and should not do — its purpose, constraints, and quality standards — as explicit documents consulted at decision points.

## Governance Patterns

### Archon / Dark Factory Pattern

- `mission.md` — what the factory should do
- `factory-rules.md` — hard constraints (e.g., max 500 lines per PR)
- Consulted on every decision by the AI

### Agent-Orchestrator Pattern

- `agent-orchestrator.yaml` — agentRules, reactions, notification routing
- `GOVERNANCE.md` + `SCOPE.md` — injected into evolve loop Phase 1 OBSERVE as constraints
- `IMPLICIT_DENY_LIST` — hard constraints
- Skeptic verdict + evidence bundle — human-auditable markdown artifacts
- Runs at startup + periodic (not on every decision)

## Key Differences

| Dimension | Archon Dark Factory | AO |
|---|---|---|
| Format | Plain English mission.md | YAML config + markdown docs |
| Timing | Every decision | Startup + periodic |
| Enforcement | AI self-enforces | Config + Skeptic verification |
| Human audit | Read the docs | Skeptic evidence bundles |

## What AO's Governance Could Learn

1. **Plain English governance docs** — mission.md / factory-rules.md style for purpose and constraints
2. **Explicit quality standards** as documents AI must reason against
3. **Compositional governance** — governance files that compose across workflows

## What Archon's Governance Could Learn

1. **Independent verification** — Skeptic's LLM-based verdict is more rigorous than self-enforcement
2. **Event-driven reactions** — human doesn't need to manually restart
3. **Evidence artifacts** — markdown bundles for human audit without querying JSON store

See [[DarkFactory]], [[Archon]], [[jleechanorg/agent-orchestrator]], [[slack-c09grlxf9gr-archon-analysis-2026-04-15]].

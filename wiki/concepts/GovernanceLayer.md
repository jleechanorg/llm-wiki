---
title: "Governance Layer"
type: concept
<<<<<<< HEAD
tags: [governance, constraints, ai-safety, policy]
=======
tags: [governance, evolve-loop, autonomous, constraints, fail-closed]
>>>>>>> origin/fix/br-4bk-green-gate-design-doc-v2
date: 2026-04-15
---

## Overview

<<<<<<< HEAD
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
=======
A governance layer defines what an autonomous agent system should and should not do — its constraints, quality standards, and escalation paths — as explicit files consulted at runtime rather than hardcoded in application logic.

## Governance as Constraints vs Checkpoints

**Checkpoint model** (Archon's Dark Factory): Human must sign off at decision gates. Pipeline stops until human approves.

**Constraint model** (AO proposal): Governance defines boundaries. System runs autonomously and self-enforces. Human can audit after the fact but never blocks forward progress.

This is the key architectural distinction in PRs #452 and #453.

## Governance in AO

| What | Where | How |
|------|-------|-----|
| IMPLICIT_DENY_LIST | `orchestrator-prompt.ts` | Hardcoded, requires code change |
| GOVERNANCE.md (proposed) | `~/.ao-evolve-knowledge/<projectId>/` | Filesystem-based, editable without PR |
| SCOPE.md (proposed) | `~/.ao-evolve-knowledge/<projectId>/` | In/out of bounds, runtime-readable |
| Skeptic verdict | JSON store (proposed: .md) | Skeptic output, optional human review |
| Evidence bundle | JSON store (proposed: .md) | Evidence artifacts, optional human review |

## Constraint Types

### Hard Constraints
Enforced, no override by agent. Example:
- Never: `gh pr merge`, `gh pr close`, `git reset --hard`, `rm -rf`
- Never: modify GOVERNANCE.md itself
- Never: disable CI checks

### Soft Constraints
Warned but can proceed. Example:
- PR max 600 lines
- Skeptic must PASS (not SKIPPED)
- Always run tests before merge

### Escalation Paths
Optional human review available, not required:
- `/escalate` command requests human review
- Auto-escalate after 3 consecutive failures

## Governance vs Evidence

| Dimension | Governance | Evidence |
|-----------|------------|----------|
| Purpose | What the system should never do | What the PR actually produced |
| Timing | Consulted at every OBSERVE cycle | Written after skeptic/evidence runs |
| Human role | Can edit constitution | Can audit artifacts |
| Blocking? | Hard = always, Soft = warn | Never blocks (fail-closed on missing) |

## Related Designs

- [[PR #452/453 Governance Layer]] — PRs #452 (runtime governance) and #453 (gate enforcement)
- [[EvolveLoop]] — the 8-phase loop that reads GOVERNANCE.md at startup
- [[DarkFactory]] — Archon's mission.md + factory-rules.md governance pattern
- [[Skeptic]] — existing Skeptic gate; SKIPPED treated as FAIL (bd-0cfv fix)
- [[EvidenceGate]] — existing evidence infrastructure
>>>>>>> origin/fix/br-4bk-green-gate-design-doc-v2

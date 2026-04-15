---
title: "Governance Layer"
type: concept
tags: [governance, evolve-loop, autonomous, constraints, fail-closed]
date: 2026-04-15
---

## Overview

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

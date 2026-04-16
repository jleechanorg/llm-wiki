---
title: "Governance Layer Research Synthesis"
type: concept
tags: [governance, autonomous, constraints, fail-closed, evidence, merge-gates]
date: 2026-04-15
---

## Summary

Research synthesis on governance layer patterns for autonomous coding agents. Combines PR #452/#453 design analysis, Grok's second opinion critique, and existing wiki concepts (SkepticGate, AutonomousAgentLoop, EvidenceBundles, CheckpointValidation).

## State of the Art

### SkepticGate (Existing AO)
- CI gate requiring per-check artifacts with timestamps (tool name, verdict, duration)
- Fails closed if evidence missing or stale
- Renamed from skeptic-gate → green-gate in PR #6189 (naming was misleading)
- Part of the [[AutonomousAgentLoop]] Five Gates: CI green, no conflicts, no serious comments, evidence reviewed, OpenClaw approved

### AutonomousAgentLoop (Existing AO)
The existing 5-gate merge-readiness model:
1. CI green — GitHub Actions `conclusion == success`
2. No conflicts — GitHub API `mergeable == MERGEABLE`
3. No serious comments — CodeRabbit/Copilot/Cursor Bugbot `REQUEST_CHANGES`
4. Evidence reviewed — CodeRabbit/Codex via `/er`
5. OpenClaw approved — `ReviewDecision.approve`

### DarkFactory / Archon (External Reference)
- Plain English governance files (`mission.md`, `factory-rules.md`)
- Consulted on every decision (coupled governance)
- Holdout validation pattern (validation agent blind to implementation)
- Level 4 system with level 5 branding

## Grok's Three Critiques of PR #452/#453

### Critique 1: Filesystem Dependency Is the Wrong Abstraction
`GOVERNANCE.md` on filesystem is a human-first mechanism. Problems:
- No versioning, no transactional writes, no audit trail
- Concurrent evolve cycles can race on file writes
- Silent degradation when fallback to IMPLICIT_DENY_LIST kicks in
- The enforcement still lives in prompt injection (code), not the file

**Alternative**: Governance as versioned, queryable policy objects in SQLite/JSONL store. Each rule: `id, created_at, author, scope, constraint_text, enabled, hit_count, override_count`. This gives metrics for free.

### Critique 2: Five Gates Is Bureaucracy, Not Engineering
PR #453's 5-gate system (CI + CR + Skeptic + Evidence + Policy) overlaps significantly:
- Evidence and Policy are subsets of what Skeptic already checks
- CR approval overlaps with Merge Gate Enforcer
- 30-minute escalation timer is arbitrary and generates false positives

**Alternative**: A single well-designed semantic evaluator that checks constraints against evidence bundle and PR metadata.

### Critique 3: No Feedback Loop, No Learning Mechanism
Neither PR addresses how governance rules improve over time:
- If a rule causes 80% of PRs to fail and require override, system never knows
- If agent writes fake evidence, no detection
- Governance is static policy, not a monitored self-correcting system

## Governance as Constraints vs Checkpoints

| Model | Human Role | Forward Progress | Archetype |
|-------|-----------|-----------------|-----------|
| Checkpoint | Required to sign off | Blocked until approval | Archon Dark Factory |
| Constraint | Can audit after | Never blocked | AO proposal |

AO's stated model is "constraint, not checkpoint" — but the 5-gate enforcement in PR #453 has checkpoint-like properties (hard gate blocks merge). The tension is in the design itself.

## Gap Analysis: What AO Has vs What's Proposed

| Layer | Exists | PR #452 | PR #453 |
|-------|--------|---------|---------|
| Hard constraints | IMPLICIT_DENY_LIST (hardcoded) | Filesystem-based | — |
| Soft constraints | agent-orchestrator.yaml reactions | Yes | — |
| Scope definition | agent-orchestrator.yaml | SCOPE.md | — |
| Skeptic verdict | JSON store | skeptic-verdict.md | Skeptic gate |
| Evidence bundle | JSON store | evidence-bundle.md | Evidence Validator |
| Escalation | stuck-worker-detector, stalled-worker-auditor | Yes | Escalation Manager |
| Merge gate | CI green + CR APPROVED | — | 5-gate Merge Gate Enforcer |
| Policy engine | agent-orchestrator.yaml | — | YAML Policy Engine |

## Key Tensions

### Tension 1: IMPLICIT_DENY_LIST vs GOVERNANCE.md
The stated goal of PR #452 is "filesystem-based, editable without PR." But the enforcement still lives in code (prompt injection). The real problem is IMPLICIT_DENY_LIST requires a code change to modify. Fixing this with filesystem files doesn't change enforcement — it only changes edit ergonomics.

**Question**: Does the enforcement mechanism actually need to change, or just the edit mechanism?

### Tension 2: Skeptic vs Merge Gate Enforcer
PR #453's Skeptic gate and Merge Gate Enforcer overlap. Skeptic already attempts semantic evaluation. The 5-gate model may be re-encoding what Skeptic does with extra bureaucracy.

**Question**: Should Skeptic be the single semantic gate, with separate Evidence Validator for artifact quality?

### Tension 3: Checkpoint vs Constraint
PR #453 says "fail-closed" but also has "escalation paths." If escalation blocks merge until human resolves, it's a checkpoint. If escalation is async notification, it's constraint.

**Question**: Is escalation a gate or a notification?

## Recommendations

1. **Single semantic gate over 5-gate committee** — Skeptic should be the authoritative semantic evaluator. Evidence Validator should check artifact quality, not re-check semantics.

2. **Governance as versioned policy objects, not files** — Hit count, override count, and author per rule give feedback loops the current design lacks.

3. **Escalation as async notification, not gate** — The system proceeds. Human is notified. If human doesn't act within N days, auto-close or auto-escalate. Never block.

4. **Separate edit mechanism from enforcement mechanism** — IMPLICIT_DENY_LIST could be moved to a JSONL store with file import/export, giving edit-ergonomics without filesystem dependency.

## Related Concepts

- [[GovernanceLayer]] — The governance layer concept page
- [[SkepticGate]] — Existing Skeptic gate infrastructure
- [[AutonomousAgentLoop]] — The 5-gate merge-readiness model
- [[EvidenceBundles]] — Evidence capture standard
- [[PR #452/453 Governance Layer]] — The design PRs being critiqued
- [[DarkFactory]] — External reference: Archon's governance approach

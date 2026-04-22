---
title: "Governance Layer Design (BFS Research + PR #452/#453)"
type: source
tags: [governance-layer, bfs-research, ao-design, converge, design-doc]
date: 2026-04-15
source_file: governance-layer-design-bfs-2026-04-15.md
---

## Summary

Synthesizes BFS research across 62+ systems and PR #452/#453 governance design into a concrete AO governance layer architecture. Key finding: collapse 5-gate committee to Skeptic (semantic) + Evidence Validator (artifact quality) + Policy Engine (constraints). Add GitOps approval workflow for GOVERNANCE.md changes. Add drift detection for governance rule self-correction via hit_count/override_count tracking. Escalation is async notification, never blocking.

## Key Claims

1. **Filesystem GOVERNANCE.md is insufficient** — needs Git-tracked version history + RBAC + audit trail. OPA-style versioned policy objects are the right model (not a file in `~/.ao-evolve-knowledge/`).
2. **5-gate committee should collapse to 3** — Skeptic (semantic), Evidence Validator (artifact quality), Policy Engine (constraints). Merge Gate Enforcer duplicates Skeptic.
3. **Escalation is async notification, never blocking** — the system proceeds. Human is notified. Auto-close or re-escalate if no action within N days.
4. **Governance needs feedback loops** — hit_count/override_count per rule. If >50% override rate, flag rule for review. RLAIF-inspired governance rule evolution.
5. **Fail-closed is non-negotiable** — Skeptic SKIPPED or missing evidence → entire PR fails closed. Confluent Schema Registry is the canonical model: "entire batch discarded if any invalid."

## Architecture: Three-Component Governance Layer

```
GOVERNANCE.md (Git-tracked constitution, PR-approved changes)
├── Hard constraints (never: gh pr merge, git reset --hard, rm -rf)
├── Soft constraints (warn: PR max 600 lines, Skeptic must PASS)
└── Escalation paths (async: /escalate, auto after 3 failures)

Gate Pipeline (executed per PR):
┌─────────────────────────────────────────────────────────┐
│ 1. Skeptic Gate     → Semantic evaluation (PASS/FAIL)  │
│ 2. Evidence Validator → Artifact quality (claim class) │
│ 3. Policy Engine     → Constraint check (OPA/Rego)     │
└─────────────────────────────────────────────────────────┘
Escalation Manager (async notification, never blocks)
Drift Detection (override_count → flag rules for review)
```

## Confluent Stream Governance as the Design Model

Confluent's three-pillar model maps to AO:

| Confluent | AO Governance |
|-----------|--------------|
| Stream Lineage | GOVERNANCE.md edit history (Git) |
| Stream Catalog | SCOPE.md (in/out of bounds per project) |
| Stream Quality | Skeptic + Policy Engine |

**Key insight**: Confluent doesn't block the stream — it marks quality and lets operators decide. AO should mark PRs as "needs review" not "blocked forever."

## Fail-Closed Validation (Canonical Model)

Confluent Schema Registry: "If a batch of messages is sent, and at least one is invalid, then the entire batch is discarded."

AO Skeptic applies the same semantics:
- Missing evidence → FAIL closed
- Skeptic SKIPPED → FAIL closed (bd-0cfv fix)
- Policy violation → FAIL closed

The Escalation Manager handles async notification path, not soft fail.

## GitOps Approval Workflow for GOVERNANCE.md

Apply Weaveworks/ArgoCD/Flux GitOps pattern to governance file changes:
- Changes to GOVERNANCE.md require PR approval (not just file edit)
- Automated sync enforces policy (same as Flux syncing cluster state)
- Audit trail is Git history, not a separate log

This addresses Grok's filesystem critique: governance isn't "a file you edit" — it's "a Git-tracked constitution with PR-based changes."

## Feedback Loop: Governance Rule Self-Correction

Stuart Russell (CHAI): "Any initial formal specification of human values is bound to be wrong in important ways."

RLAIF-inspired governance evolution:
- Human override logged → hit_count/override_count increment
- If override_count > 50% of hit_count → flag rule for review
- Rule reviewed → updated or removed
- Drift Detection (Arize/Phoenix model) monitors governance outcomes

This gives the governance layer what PR #452/#453 lacks: a learning mechanism.

## Key Quotes

> "If a batch of messages is sent, and at least one is invalid, then the entire batch is discarded." — Confluent Schema Registry (fail-closed model)

> "AI systems should be uncertain of their objectives, and should be deferent to humans." — Stuart Russell / CHAI (governance philosophy)

> "Agents are generalists by design, and they don't inherently know the best practices and design patterns that real-world production systems demand." — MongoDB Agent Skills (why governance matters)

> "Stream governance enables data in motion, giving real-time data governance tools built to help foster secure, compliant, and scalable collaboration." — Confluent (three-pillar model)

## Connections

- [[GovernanceLayerResearch]] — Grok's 3 critiques + recommendations
- [[SkepticGate]] — existing Skeptic gate (semantic evaluator)
- [[EvidenceBundles]] — evidence artifact infrastructure
- [[OPA]] — Policy Engine candidate (Rego language)
- [[Confluent]] — Stream Governance model
- [[GitOps]] — GOVERNANCE.md change approval pattern
- [[DriftDetection]] — governance rule self-correction
- [[RLAIF]] — governance rule learning mechanism
- [[FailClosedValidation]] — Confluent's fail-closed semantics
- [[DarkFactory]] — Archon's coupled governance (contrast to AO's decoupled)
- [[AutonomousAgentLoop]] — the 8-phase loop this governance extends
- [[StreamGovernance]] — Confluent's three-pillar model
- [[ValueAlignment]] — CHAI philosophy for governance design

## Open Questions

1. Should OPA/Rego be the Policy Engine, or a simpler YAML constraint system?
2. What is the N-day auto-close threshold for escalation with no human action?
3. Who can approve GOVERNANCE.md changes? (ACL design)
4. Global vs per-project GOVERNANCE.md precedence?
5. How does Skeptic interop with Policy Engine — same turn or sequential?

## See Also
- [[GovernanceLayerResearch]]
- [[GovernanceLayer]]
- [[SkepticGate]]
- [[OPA]]
- [[DriftDetection]]
- [[GitOps]]
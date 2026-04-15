---
title: "Governance Layer Design (PRs #452, #453)"
type: source
tags: [governance-layer, evolve-loop, ao-design, autonomous-merge, skeptic]
date: 2026-04-15
source_file: pr-452-453-governance-layer-design-2026-04-15.md
---

## Summary

Two companion design PRs (#452 docs/feat/governance-layer, #453 docs: real-time-governance-layer) propose adding a governance layer to the AO evolve loop. PR #452 focuses on runtime governance files (GOVERNANCE.md, SCOPE.md) readable every OBSERVE cycle. PR #453 proposes a 4-component gate-governance plugin (Evidence Validator, Merge Gate Enforcer, Escalation Manager, Policy Engine). Both maintain the constraint: no mandatory human review, system proceeds autonomously unless a hard constraint is violated.

## Key Claims

- AO's 8-phase evolve loop (OBSERVE → MEASURE → DIAGNOSE → PLAN → FIX → GROOM → COMMIT → REVIEW) already has governance infrastructure, but constraints are hardcoded in orchestrator-prompt.ts
- Current merge criteria (CI green + CodeRabbit APPROVED) is insufficient for safe autonomous merging
- Governance should be filesystem-based (GOVERNANCE.md), editable without code changes or PRs
- Skeptic SKIPPED should be treated as FAIL (fail-closed), fixing bd-0cfv
- Escalation routes to human intervention but never blocks autonomous progression
- The two PRs are complementary: #452 is the constitution (runtime reads), #453 is the enforcement (gate plugin)

## Architecture (PR #453)

```
Governance Layer
├── Evidence Validator → checks artifacts/, test logs, claim class
├── Merge Gate Enforcer → 5-gate: CI + CR + Skeptic + Evidence + Policy
├── Escalation Manager → inactivity >30min, /escalate command
└── Policy Engine → YAML per-project governance rules
```

## Runtime Governance Structure (PR #452)

```
~/.ao-evolve-knowledge/<projectId>/
├── GOVERNANCE.md     # Hard constraints (IMPLICIT_DENY_LIST replacement)
├── SCOPE.md          # In/out of bounds for issues
└── prs/<prNumber>/
    ├── skeptic-verdict.md   # Skeptic output, optional
    └── evidence-bundle.md   # Evidence bundle, optional
```

## Key Quotes

> "The system does not wait for a human. Ever. Human can open the file and look but the loop always keeps running." — openclaw_staging (2026-04-15)

> "Governance as constraints, not checkpoints." — openclaw (2026-04-15)

> "Your AO already has a significantly more sophisticated system than Coles. The 8-phase loop, the IMPLICIT_DENY_LIST, the spawn queue, the merge gate, the skeptic is already superior to what Cole built." — openclaw_staging (2026-04-15)

## Open Questions

1. Should governance run before or after CodeRabbit?
2. Should `chore`/`docs` PRs be exempt from evidence requirements?
3. Should escalation auto-close PRs after N days with no human action?
4. Sync governance files to git?
5. Global vs per-project GOVERNANCE.md precedence?
6. Who can edit GOVERNANCE.md? (ACL?)

## Connections

- [[jleechanorg/agent-orchestrator]] — the repo this governance layer is designed for
- [[EvolveLoop]] — the 8-phase loop this governance layer extends
- [[GovernanceLayer]] — concept page for governance as constraints vs checkpoints
- [[DarkFactory]] — Cole's Archon governance approach (mission.md + factory-rules.md)
- [[Skeptic]] — existing Skeptic gate that SKIPPED=success bug needs fixing
- [[EvidenceGate]] — existing evidence infrastructure

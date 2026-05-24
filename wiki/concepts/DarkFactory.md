---
title: "Dark Factory"
type: concept
tags: [autonomy, governance, workflow, archon]
date: 2026-04-15
---

## Overview

Dark Factory is Cole's (coleam00) governance-heavy autonomous workflow concept built on Archon. It implements a 3-worktree pipeline for processing GitHub issues without continuous human oversight.

## Architecture

```
Triage workflow → Implementation workflow → Validation workflow
     (fresh worktree)      (archon-fix-github-issue)    (holdout validation)
```

### Governance Files

- `mission.md` — what the factory should do
- `factory-rules.md` — 320 lines of constraints including max 500 lines per PR as a hard constraint

### Pipeline Details

1. **Triage workflow** reads new GitHub issues, filters against mission.md and factory-rules.md
2. **Implementation workflow** (archon-fix-github-issue) runs in a fresh worktree
3. **Validation workflow** uses holdout pattern — validation agent blind to implementation

## Autonomy Claims vs Reality

| Claim | Reality |
|---|---|
| Level 5 autonomy | Level 4 — human must monitor and restart |
| No steering wheel | Human manually kicks off workflows |
| Fully autonomous | Fail-closed: SKIPPED is not PASS |

Cole is honest about limits on stream, but framing (dark factory, no steering wheel, level 5) implies more autonomy than reality.

## What It Gets Right

1. Governance as plain English documents consulted at decision points
2. Holdout validation pattern — independent verification blind to implementation
3. Opinionated starting-point templates
4. Max PR size as a hard-enforced constraint

## vs Agent-Orchestrator Evolve Loop

| Dimension | Dark Factory | AO Evolve Loop |
|---|---|---|
| Governance timing | On every decision | At startup + periodic |
| Parallel worktrees | Per issue | Per PR, N parallel |
| Zero-touch window | None — human monitors | 6hr target |
| Independent verification | Holdout pattern | Skeptic LLM |
| Failure recovery | Implicit retry hooks | Explicit: stuck-worker-detector, stalled-worker-auditor, parallel-retry |

See [[Archon]], [[jleechanorg/agent-orchestrator]], [[slack-c09grlxf9gr-archon-analysis-2026-04-15]].

## vs Four Canonical Attractor Implementations

The dark-factory (Python) is one of five Attractor pattern implementations. Four independent implementations converged on the same three-layer architecture (LLM client → Agent loop → Pipeline engine), confirming structural correctness.

| Dimension | dark-factory | [[AttractorBench]] | [[Kilroy]] | [[Smasher]] | [[Mammoth]] |
|---|---|---|---|---|---|
| Language | Python | Python | Go | Rust | TypeScript |
| Parallel | No | Yes (Harbor) | Yes (4 join policies) | Yes (bounded) | TBD |
| Multi-model | Single backend | Single provider | CSS stylesheet + escalation | 3 providers + catalog | TBD |
| Holdout | Sealed repo + sandbox-exec | Sealed mock LLM + LLM Judge | review_consensus | Tiered conformance | TBD |

**dark-factory is unique** in having:
- Healer failure clustering (no other implementation has post-hoc failure clustering)
- /es /er /code_standards slash gates with SHA binding
- Sealed holdouts via `$DARK_FACTORY_HOLDOUTS` + `sandbox-exec`

**dark-factory is the ONLY one** without parallel execution. Its engine walks a single path sequentially via `_edge_matches`.

For the full feature-by-feature gap analysis, see source page `attractor-four-implementation-gap-analysis-2026-05-24`.

See [[AttractorPattern]], [[ModelStylesheet]], [[AttractorParallelExecution]], [[FailureDossier]].

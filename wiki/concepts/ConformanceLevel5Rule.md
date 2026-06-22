---
title: "Conformance Level5 Rule"
type: concept
tags: [dark-factory, dot-engine, conformance, level5, invariants]
date: 2026-06-22
sources:
  - /Users/jleechan/llm_wiki/raw/project_2026-06-22_g3_closure_dynamic_node_design.md
last_updated: 2026-06-22
---

# Conformance Level5 Rule

## Overview

An extension to `bin/conformance validate` that enforces the structural invariants required for a Dark Factory pipeline to be a Level-5 (dark factory) operation. Separates the gates into two tiers: hard-guaranteed (always-on, runner refuses to start the pipeline without them) and soft-guaranteed (default-present, opt-out via `skip_<x>="true"`).

## Hard Tier — runner refuses to start without them

| # | Invariant | Role |
|---|---|---|
| 1 | **CXDB event log** (instrumentation, not a node) | Every step recorded; Level-5 audit trail |
| 2 | **`gate_er`** | Evidence review — every claim backed by a bundle |
| 3 | **`gate_skeptic`** | Independent inverted-incentive review |
| 4 | **`adversarial_reviewer`** | Cross-vendor LLM verdict (codex > minimax > agy > claude-sonnet) |

The runner refuses to start a `level5` pipeline if any of these are missing. No flag to bypass.

## Soft Tier — default-present, `skip_<x>="true"` opt-out

| # | Node | Skip when |
|---|---|---|
| 5 | `holdout_eval` | `skip_holdout="true"` only when no production code is touched |
| 6 | `healer` | Only fires on terminal failure (no skip flag needed) |
| 7 | `spec_validation` | `skip_spec_validation="true"` when iterating on an existing spec |

The runner warns (not errors) if these are missing without an explicit skip flag.

## Scope

Applies to:
- Every pipeline matching `pipelines/factory/*.dot`
- Every `.dot` with `level5="true"` on the graph itself

Exempt (smoke / iteration lanes):
- `pipelines/slim/*.dot`
- `pipelines/factory/hello.dot`

## Why it lives in conformance, not the runner

The runner stays dumb — the hot path is dispatch + CXDB + perf log, not invariant validation. Conformance-validate is a separate, pre-flight check that runs before the runner starts. This keeps the runner fast and lets authors run un-validated `.dot` files in dev mode for exploration.

## Why two tiers

- **Hard tier (4) = structural invariants** that make the system trustworthy. Drop any one and you've quietly downgraded from Level-5 (dark factory) to a fancier test harness.
- **Soft tier (3) = policy defaults** that almost every `factory/*.dot` should follow, but which have legitimate opt-outs (docs-only PR, no production code, iterating on existing spec).

The hard tier is the "minimum bar to be Level-5." The soft tier is "best practice; opt out with explanation."

## Connections

- [[DOTAsArtifact]] — the `.dot` is the artifact; conformance enforces the structural shape.
- [[DynamicNodeType]] — the new node kind that requires the `default="<static>"` reference (conformance checks it).
- [[CXDB]] — hard-tier invariant #1, always-on instrumentation.
- [[AdversarialReviewPriorityQueue]] — the priority queue used by `adversarial_reviewer`.
- [[Level5AutonomyReview]] — the audit that surfaced the gaps the hard tier closes.
- [[HealerAgent]] — soft-tier node #6; runs on terminal failure.
- [[DarkFactoryOperatingMode]] — the repo's tenets this rule set encodes structurally.

## Example error

```text
$ bin/conformance validate pipelines/factory/my_feature.dot
ERROR: pipelines/factory/my_feature.dot is missing required hard-tier node 'gate_er'
ERROR: pipelines/factory/my_feature.dot is missing required hard-tier node 'gate_skeptic'
ERROR: pipelines/factory/my_feature.dot is missing required hard-tier node 'adversarial_reviewer'
ERROR: type="dynamic" node 'explore' has no default="<static_node>" attribute (required)
3 hard-tier violations, 1 dynamic-node contract violation.
Refusing to start.
```

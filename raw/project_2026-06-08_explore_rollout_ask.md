---
name: dark-factory-explore-phase-rollout-ask-2026-06-08
description: "User explicitly asked to extend the explore->plan gate (commit 6c6a2a3, slim-only) to all non-gate, non-review pipelines. 5 of 7 .dot files still lack explore."
metadata: 
  node_type: memory
  type: project
  originSessionId: 3841c15c-39a4-4af3-bca9-6c051dff9052
---

Commit `6c6a2a3` ("feat(slim): add explore phase and role-based model routing") introduced a mandatory `explore -> plan` gate inside `pipelines/slim/minimal_feature.dot` and `pipelines/slim/minimal_pr.dot`. After reviewing the commit, the user said verbatim: **"also i want explore for all the pipelines not just one"**.

**Pipeline inventory (7 .dot files):**

| Pipeline | Has `explore`? | Action |
|---|---|---|
| `pipelines/slim/minimal_feature.dot` | yes | canonical (unchanged) |
| `pipelines/slim/minimal_pr.dot` | yes | canonical (unchanged) |
| `pipelines/factory/hello.dot` | no | **add explore** (primary) |
| `pipelines/factory/gates.dot` | no | optional behind `--state factory.explore=true` |
| `pipelines/factory/pr_gates.dot` | no | out of scope (gate-only) |
| `pipelines/parallel_demo.dot` | no | out of scope (demo) |
| `pipelines/slim/review_pr.dot` | no | out of scope (review-only) |

**Role-routing stylesheet shape** (`pipelines/slim/minimal_feature.model.css`): `explore`/`implement`/`fix` honor run-level `--backend` (coder tier); `plan` pinned to `claude-opus-4-6` (should become `DARK_FACTORY_PLAN_MODEL` env var per jleechan-x57); `review` routed to agy (independent reviewer).

**Beads filed for this rollout:**
- `jleechan-2wx` (P1) — propagate to `factory/hello.dot` (and selectively `factory/gates.dot`); GH issue [#18](https://github.com/jleechanorg/dark-factory/issues/18)
- `jleechan-80r` (P3) — explore early-exit on infeasible verdict; GH [#19](https://github.com/jleechanorg/dark-factory/issues/19)
- `jleechan-x57` (P3) — `DARK_FACTORY_PLAN_MODEL` env var; GH [#20](https://github.com/jleechanorg/dark-factory/issues/20)
- `jleechan-4gx` (P3) — clean up two untracked leftovers from prior sessions; GH [#21](https://github.com/jleechanorg/dark-factory/issues/21)

**Why:** The explore gate is supposed to be the dark-factory default, not a slim-only special case. The role-routing stylesheet is the right pattern — coder/plan/review tiers — and should be the cross-pipeline default.

**How to apply:** When authoring any new dark-factory `.dot` pipeline that has a `plan` step, the explore node precedes plan and the role-routing stylesheet references the role table. The slim/minimal_feature.dot shape is the canonical template.

---
title: "G3 closure design — type=dynamic + claude -p --effort high (Dark Factory 2026-06-21)"
type: source
tags: [dark-factory, dot-engine, dynamic-workflows, level5, design-decision]
date: 2026-06-22
source_file: /Users/jleechan/llm_wiki/raw/project_2026-06-22_g3_closure_dynamic_node_design.md
---

# Source: G3 closure design — type="dynamic" + claude -p --effort high (Dark Factory 2026-06-21)

- **Type**: project / design-decision
- **Date**: 2026-06-21 (locked), 2026-06-22 (memory capture)
- **Origin**: Dark Factory — brainstorm session on integrating Claude Code's native Dynamic Workflows into the static `.dot` engine
- **Raw**: `~/llm_wiki/raw/project_2026-06-22_g3_closure_dynamic_node_design.md`
- **Claude memory**: `/Users/jleechan/.claude/projects/-Users-jleechan-projects-dark-factory/memory/project_2026-06-22_g3_closure_dynamic_node_design.md`
- **Bead**: jleechan-0qy (open, implementation tracking)
- **Related references**:
  - `reference_2026-06-21_official_dynamic_workflows_vs_dotfactory.md` (the G3 gap this closes)
  - `project_2026-06-04_workflow_graphgen_spec.md` (n=10 benchmark, no separation on any axis)
  - `project_2026-06-05_dynamic_fanout_calibration.md` (G3 was the real paradigm gap)
  - `project_2026-06-09_level5_autonomy_review.md` (Level-5 autonomy = the goal)

## Summary

The Dark Factory `.dot` runner is itself an orchestrator, so Claude Code's native Dynamic Workflows (Workflow tool / ultracode / `.claude/workflows/`) is a **competing** orchestrator, not a missing dependency. The repo's own n=10 Sonnet benchmark showed dynamic dispatch gives no separation on any axis and is ~5–9% slower for first-pass coding tasks while losing the durable versioned artifact. The single structural gap (G3 = runtime-determined fan-out) is now closed by a new `type="dynamic"` node attribute that dispatches via `claude -p --effort high` (high effort, NOT ultracode) when the driver is Claude Code, and falls back to a static `default="<node>"` codergen when the driver is any other CLI. Both paths run at `--effort high` (option a: full parity). Hard tier (always-on): CXDB + `gate_er` + `gate_skeptic` + `adversarial_reviewer`. Soft tier (default-present, `skip_<x>="true"` opt-out): `holdout_eval` / `healer` / `spec_validation`. Enforcement via extended `bin/conformance validate` against `pipelines/factory/*.dot` and any `.dot` with `level5="true"`.

## Key Claims

- Dark Factory should NOT adopt native Dynamic Workflows as its primary orchestrator — the n=10 benchmark shows no benefit and the cost is losing the durable `.dot` artifact.
- The G3 gap (runtime-determined fan-out) is closed by `type="dynamic"` nodes that shell `claude -p --effort high` (not ultracode / Workflow tool), giving Claude high-effort latitude to re-plan substeps inside a single session.
- Driver-based dispatch: when driver=claude_code → `claude -p --effort high` with auto-wrap; when driver≠claude_code → resolve `default="<static_node>"` and run as `codergen`. Both at high effort (option a).
- Every dynamic node requires `default="<node_name>"` — conformance check enforces it; no dynamic node can exist without a static fallback.
- Hard tier (4) is structural: CXDB event log + `gate_er` + `gate_skeptic` + `adversarial_reviewer`. The runner refuses to start a `level5` pipeline without them.
- Soft tier (3) is policy: `holdout_eval` (skip when no prod code), `healer` (only fires on terminal failure, no skip needed), `spec_validation` (skip when iterating on existing spec).
- Enforcement lives in `bin/conformance validate` (not the runner's hot path). `pipelines/slim/*.dot` and `pipelines/factory/hello.dot` are exempt.

## Key Quotes

> "Mechanism: Option 1 (runner shells `claude -p --effort high` for dynamic nodes). NOT ultracode / Workflow tool. The runner stays the single orchestrator."

> "Trigger: When the driver is Claude Code (in-session, has native Workflow tool), use the dynamic path. When the driver is any other CLI (codex / ao / agy), fall back to the existing Python `.dot` runner. The `.dot` stays the durable spec in both paths."

> "Both paths use `--effort high` (option a: full parity). The only thing that changes between drivers is who runs the model, not how hard it thinks."

> "Hard tier (always-on): CXDB event log (instrumentation, not a node — built into the runner); gate_er — evidence review; gate_skeptic — inverted-incentive review; adversarial_reviewer — cross-vendor LLM verdict."

## Connections

- [[DynamicWorkflowsNativeVsDotEngine]] — the G3 gap this design closes
- [[WorkflowGraphgenBenchmark]] — n=10 measurement showing no separation between dynamic vs static dispatch
- [[DynamicFanoutCalibration]] — G1-adjacent works via `${state._last_output}` (authoring choice); G3 was the real paradigm gap
- [[Level5AutonomyReview]] — Level-5 autonomy = the goal this design serves
- [[FactoryEvolveSkill]] — factory-evolve roadmap includes Level-5 gate wiring
- [[AdversarialReviewPriorityQueue]] — `codex > minimax > agy > claude-sonnet` is the priority queue for `adversarial_reviewer` node
- [[HealerFailureClusters]] — `healer` is the soft-tier post-failure node, only fires on terminal failure
- [[ConformanceValidate]] — enforcement surface for the level5 rule set
- [[CXDBEventLog]] — hard-tier invariant, always-on instrumentation
- [[RunnerHandlers]] — the dispatch code path lives in `runner/handlers.py`

## Implementation

Bead **jleechan-0qy** tracks the work. Scope:

1. Add `type="dynamic"` handler in `runner/handlers.py` with driver-based dispatch.
2. Add `_wrap_dynamic_prompt` helper (auto-wrap template).
3. Extend `bin/conformance validate` with the level5 rule set.
4. Add `pipelines/factory/level5_feature.dot` reference.
5. Migrate `pipelines/factory/gates.dot` to the new convention (rename + wrap `explore` / `plan` / `implement` / `fix` with `type="dynamic"`).
6. Tests: dispatch (claude_code vs non-claude_code), fallback, conformance rule, auto-wrap.

## Notes

Also surfaced a pre-existing br bug: `.beads/beads.db` had a stale `issue_prefix=dark-factory` value overriding the project config file's `jleechan`. Fix: `UPDATE config SET value='jleechan' WHERE key='issue_prefix'`. This unblocked all `br create` invocations.

---
name: g3-closure-design-type-dynamic-nodes-claude-p-effort-high
description: "Locked design (2026-06-21) for closing the G3 (runtime-determined fan-out) gap via runner-shell claude -p --effort high dispatch, two node flavors, hard+soft guaranteed tiers, and conformance-validate enforcement."
metadata: 
  node_type: memory
  type: project
  bead: jleechan-0qy
  originSessionId: 920b327c-81fc-433b-ba74-31dbed1aa7de
---

# G3 closure design — `type="dynamic"` nodes + `claude -p --effort high`

## Why this design exists

The repo deliberately does NOT use Claude Code's native Dynamic Workflows (Workflow tool / ultracode / `.claude/workflows/`) as its primary orchestrator because it IS the orchestrator (a static `.dot` engine). The repo's own n=10 Sonnet benchmark (`workflow_graphgen` + `dynamic_fanout` sweep) showed dynamic dispatch gives **no separation on any axis** and is **~5–9% slower** for first-pass coding tasks, while losing the durable versioned artifact. This is empirically defended, not an oversight.

The single structural gap (G3) = runtime-determined fan-out. This design closes that gap honestly: the repo stays a static `.dot` engine, gains native dynamic node execution when Claude Code drives `/f`, and the `.dot` remains the durable versioned artifact. See [[reference_2026-06-21_official_dynamic_workflows_vs_dotfactory]] for the gap analysis; [[project_2026-06-04_workflow_graphgen_spec]] for the n=10 benchmark; [[project_2026-06-05_dynamic_fanout_calibration]] for the G1/G3 sweep; [[project_2026-06-09_level5_autonomy_review]] for the Level-5 goal this serves.

## Locked decisions (ratified 2026-06-21)

**Trigger.** When the driver is Claude Code (in-session, has native Workflow tool), use the dynamic path. When the driver is any other CLI (`codex` / `ao` / `agy`), fall back to the existing Python `.dot` runner. The `.dot` stays the durable spec in both paths.

**Mechanism.** Option 1: the runner shells `claude -p --effort high` for dynamic nodes. **NOT** ultracode / Workflow tool. The runner stays the single orchestrator. Option 2 (split orchestration into `/f` skill) was rejected because it splits CXDB / Healer / perf-log instrumentation in a way that will bite later. Option 3 (saved `.claude/workflows/`) was rejected because it trades runtime dynamism for durability, which n=10 said you don't gain.

**Node flavors.**
- `type="codergen"` (static / default) — fixed shape, run as today
- `type="dynamic"` (runtime-shaped) — Claude with high effort re-plans substeps inside one session
- Every dynamic node requires `default="<static_node_name>"` — the fallback for non-Claude drivers

**Dispatch path** (`runner/handlers.py`):
- `type="dynamic"` + driver=claude_code → shell `claude -p --effort high` with auto-wrapped prompt
- `type="dynamic"` + driver≠claude_code → resolve to the `default` static node, run as `codergen`
- **Both paths use `--effort high`** (option a: full parity). The only thing that changes between drivers is **who** runs the model, not **how hard it thinks**.

**Auto-wrap template** (injected above the authored prompt body by `_wrap_dynamic_prompt`):

> You are a dynamic node in a Level-5 dark-factory pipeline. You may re-plan substeps, expand or compress work as you see fit. The runner will record your output to CXDB; downstream nodes consume `ctx.state`.

**Hard-guaranteed tier** (runner refuses to start a `level5` pipeline without them; always-on):
1. **CXDB event log** (instrumentation, not a node — built into the runner)
2. **`gate_er`** — evidence review
3. **`gate_skeptic`** — inverted-incentive review
4. **`adversarial_reviewer`** — cross-vendor LLM verdict via the `codex > minimax > agy > claude-sonnet` priority queue (established in [[project_2026-06-09_level5_autonomy_review]] / [[project_2026-06-09_priority_queue_dispatch]] / [[project_2026-06-09_pr26_production_verify]])

**Soft-guaranteed tier** (default-present; `skip_<x>="true"` opt-out):
5. **`holdout_eval`** — `skip_holdout="true"` only when no production code is touched
6. **`healer`** — only fires on terminal failure (no skip flag needed; the runner handles it)
7. **`spec_validation`** — `skip_spec_validation="true"` when iterating on an existing spec

**Dynamic nodes (the rest).** `explore`, `plan`, `implement`, `fix` loops; task-specific substeps. The model re-shapes these at runtime with high effort — this is the "dynamic" surface.

## Enforcement

Extend `bin/conformance validate` with a `level5` rule set. The runner stays dumb; the invariants live in the conformance surface where the repo's other invariants already live. For every pipeline matching `pipelines/factory/*.dot` (and any `.dot` with `level5="true"` on the graph itself), the rule set requires the 4 hard-tier nodes. `pipelines/slim/*.dot` and `pipelines/factory/hello.dot` are exempt (smoke / iteration lanes).

## Reference shape

`pipelines/factory/level5_feature.dot` — the reference implementation. Existing `pipelines/factory/gates.dot` is already close; the migration is just renaming nodes to the new convention and wrapping the implementation steps (`explore` / `plan` / `implement` / `fix`) with `type="dynamic"` and `default="<static>"`.

```dot
explore    [type="dynamic", default="explore_static",    prompt="@prompts/explore.md",    max_visits="2"]
plan       [type="dynamic", default="plan_static",       prompt="@prompts/plan.md",       max_visits="2"]
implement  [type="dynamic", default="implement_static",  prompt="@prompts/implement.md",  max_visits="3"]
fix        [type="dynamic", default="fix_static",        prompt="@prompts/fix.md",        max_visits="3"]
explore_static    [type="codergen", prompt="@prompts/explore.md"]
plan_static       [type="codergen", prompt="@prompts/plan.md"]
implement_static  [type="codergen", prompt="@prompts/implement.md"]
fix_static        [type="codergen", prompt="@prompts/fix.md"]
```

## How to apply

- **Adding a pipeline under `pipelines/factory/`:** the conformance check will reject it without the 4 hard-tier nodes. Plan to include `gate_er`, `gate_skeptic`, `adversarial_reviewer`, and CXDB (built-in).
- **Promoting a `pipelines/slim/` pipeline to factory:** re-enable the 3 soft-tier nodes (drop `skip_<x>="true"`); add the 4 hard-tier nodes.
- **Adding a new dynamic node:** `default="..."` is required (conformance check).
- **Dispatching a dynamic node:** the driver check decides `claude -p --effort high` (driver=claude_code) vs static fallback (driver≠claude_code). Both at high effort.
- **Conformance surface:** all invariants live in `bin/conformance validate`, not in the runner's hot path.

## Status

Design locked 2026-06-21. Implementation tracked by bead **jleechan-0qy**. Implementation plan + execution via subagents (per user directive; `/integrate` does not plan). See [[project_2026-06-21_factory_evolve_skill]] for the factory-evolve roadmap context.

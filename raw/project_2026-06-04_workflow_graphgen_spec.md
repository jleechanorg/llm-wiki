---
name: project_2026-06-04_workflow_graphgen_spec
description: workflow_graphgen A-vs-A+B benchmark IMPLEMENTED + smoke-run done; committed on feat_workflow-graphgen-benchmark (unpushed).
metadata: 
  node_type: memory
  type: project
  originSessionId: 96237b72-565c-4c2d-b265-b151de9c2353
---

`workflow_graphgen` feature = new default graph-construction mode where a Claude **Workflow** (Opus) generates a per-goal pipeline graph with pinned guaranteed reviewer nodes + dynamic middle, plus a benchmark comparing **Mode A** (runner walks every node) vs **Mode A+B** (Workflow runs the dynamic middle via `agent()`, runner runs the guaranteed-node tail). Single independent variable = who executes the dynamic middle.

**Spec status (2026-06-04): cold-reviewer PASS at iteration 3.** Two specs on disk:
- `specs/workflow_graphgen.md` (main, 11 sections)
- `benchmarks/attractor-spec-review/spec/workflow_graphgen.feature.md` (attractor line-aware; passes `validate_spec.py`, 186/186 reviewable, ratio 1.0)
- Sign-off artifact: `spec_review/workflow_graphgen_reviewer.json` (verdict pass).

**Implementation DONE + smoke-run done (2026-06-05), committed on `feat_workflow-graphgen-benchmark` (2 commits, UNPUSHED):**
- `ae85558` feat(benchmark): workflow_graphgen — `benchmarks/workflow_graphgen/{graph_ir,generator,catalog,harness,scoring,__main__}.py` + README; `prompts/catalog.json` + `prompts/catalog/*.md` (8 vocab types); `model_name` passthrough in `runner/handlers.py`; honest coder token capture (claude codergen runs `--output-format json`, `_claude_json_result` sums fresh+cache_read+cache_creation into tokens_in since `input_tokens` undercounts under prompt caching, keeps cache split + total_cost_usd); tests for model_name/catalog/harness/scoring + JSON token envelope.
- `2c1e48b` fix(parser): `_MARKER_RE` gap restricted to decoration + qualifier-tokens (no arbitrary prose) so "verdict: not a fail" no longer lifts embedded "fail" → ("unknown","failure"); fixed the 2 long-standing hardening failures; **full suite now 141 green incl. the conformance `score` self_test meta-check.**

**Smoke result (claude/Sonnet, hello+roman, 1 trial, both modes):** 4/4 records, 0 tracebacks, honest cache-inclusive tokens (hello/A 155.7k in, A+B 195.3k; roman/A 235.4k, A+B 196.7k total). §11.4 cost axis is **feature-dependent** (A wins hello, A+B wins roman — NOT a foregone conclusion); zero_touch 1.0 both modes; conformance + graph_quality "insufficient data" (no sealed evaluator wired in smoke; fit unscored at n=1). Artifacts: `/tmp/wfgg-smoke/records.jsonl` + `records.aggregate.json`.

**REAL MEASUREMENT DONE (2026-06-05), committed `80ab95e` on `feat_workflow-graphgen-benchmark` (UNPUSHED):** n=10 × 2 features × 2 modes = 40 real Sonnet runs, middle-only (`--no-spine`), `--conformance local`. **Result: NO separation on ANY axis at n=10.** conformance 50/50 & 90/90 both modes (perfect tie — both produce correct code); tokens_total ranges overlap (the smoke's "A wins hello / A+B wins roman" was pure n=1 model variance, sd≈27k–40k — the new `MIN_N_FOR_WINNER=5` + range-non-overlap guard correctly refused to crown it); wall_ms A+B directionally slower (+5.3% hello, +9.2% roman, harness dispatch overhead) but overlaps → not credited; graph_quality mode-invariant by construction (shared IR). **Honest finding: dispatch path is irrelevant for tasks the model solves first-pass; does NOT generalize to fix-loop tasks (next experiment).** Instrument added this commit: `conformance_local.py` (self-contained public-criteria evaluator — no sealed repo, no isolation break), scoring min-n guard + variance stats + wall_ms axis, `--spine/--no-spine`, `RESULTS.md`, raw evidence force-added under `benchmarks/workflow_graphgen/results/` (gitignored dir). Key unlock: hello/roman acceptance criteria are PUBLIC (in the goal text) → conformance is scoreable WITHOUT the sealed repo. Token axis is uncounfounded because `plan`/`implement` interpolate only `${goal}` (parity test guards it). Full suite 153 green.

**PR #16 status (2026-06-05): 7-GREEN at HEAD `56bb22a`.** 24 Bugbot/CR comments fixed across 7 push iterations; all threads resolved; CI=test+skeptic=success, Cursor Bugbot check=success, CR=APPROVED, 219 tests passing, unresolved=0, mergeable=MERGEABLE. Key fixes: exploratory flag through CLI (non-claude backends auto-labeled), evaluator soft-error handling (available=False for subprocess crashes), conformance_local error field propagation.

**Next:** merge PR #16; fix-loop task variant (where A+B per-node control could actually diverge); higher-n wall_ms if a latency claim is needed.

**Key fairness invariants the specs encode** (don't regress when implementing): guaranteed reviewers are **terminal** (goal_gate unset + unconditional edge to exit; `goal_gate=true` is the engine's RETRY trigger at `engine.py:_goal_gate_target` ~L1131, honors node- AND graph-level `retry_target`); graph_quality scores the shared graph-IR with 30% fit scored once-per-goal and reused for both modes; token parity = coder-execution tokens only, identical fields; baseline_ref diff handoff; fair head-to-head restricted to claude/Sonnet (other backends Mode-A-only exploratory).

Related: [[project_2026-05-24_attractor_four_implementation_gap_analysis]], [[feedback_2026-05-31_runner_resilience_reviewer_gates]].

**Cold-reviewer op-lesson:** canonical `review_with_codex.sh` / direct `codex exec --yolo` were flaky (parse-fail then 360s timeout on ~16k-char prompt) — fell back to a fresh `general-purpose` Claude subagent as the independent cold reviewer (CLAUDE.md tenet 3 allows "codex exec, AO worker, or equivalent"). Subagent's final JSON does NOT surface in the foreground Agent return (only the git-header line shows); retrieve it via `TaskOutput` on the agentId, or `SendMessage` asking for verbatim JSON then `TaskOutput`.

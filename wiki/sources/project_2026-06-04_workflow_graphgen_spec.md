---
title: "Workflow Graphgen Spec + n=10 Null (2026-06-04)"
type: source
tags: [dark-factory, workflow-graphgen, ab-benchmark, cold-review, sonnet, dispatch-mode]
date: 2026-06-04
source_file: raw/project_2026-06-04_workflow_graphgen_spec.md
---

## Summary
`workflow_graphgen` = new default graph-construction mode where a Claude Workflow (Opus) generates a per-goal pipeline graph with pinned guaranteed reviewer nodes + dynamic middle, plus a benchmark comparing Mode A (runner walks every node) vs Mode A+B (Workflow runs the dynamic middle via `agent()`, runner runs the guaranteed-node tail). Spec PASSED cold-review at iteration 3; implementation DONE; n=10 × 2 features × 2 modes = 40 real Sonnet runs returned NO separation on ANY axis — honest finding: dispatch path is irrelevant for tasks the model solves first-pass.

## Key Claims
- **Single independent variable = who executes the dynamic middle** (Mode A vs Mode A+B).
- Spec on disk: `specs/workflow_graphgen.md` (11 sections) + `benchmarks/attractor-spec-review/spec/workflow_graphgen.feature.md` (186/186 reviewable, ratio 1.0).
- Implementation commit `ae85558`: full benchmark scaffold + honest coder token capture (claude codergen runs `--output-format json`, `_claude_json_result` sums fresh+cache_read+cache_creation since `input_tokens` undercounts under prompt caching, keeps cache split + `total_cost_usd`).
- Parser fix `2c1e48b`: `_MARKER_RE` gap restricted to decoration + qualifier-tokens so "verdict: not a fail" no longer lifts embedded "fail" → ("unknown","failure"); full suite now 141 green.
- n=10 result (commit `80ab95e`): conformance 50/50 & 90/90 both modes (perfect tie); tokens_total ranges overlap (smoke's "A wins hello / A+B wins roman" was pure n=1 model variance, sd≈27k–40k); wall_ms A+B +5.3%/+9.2% but overlaps → not credited; graph_quality mode-invariant by construction (shared IR).
- **Key fairness invariants:** guaranteed reviewers are terminal (goal_gate unset + unconditional edge to exit; `goal_gate=true` is engine's RETRY trigger at `engine.py:_goal_gate_target` ~L1131, honors node- AND graph-level `retry_target`); graph_quality scores shared graph-IR with 30% fit scored once-per-goal; token parity = coder-execution tokens only; baseline_ref diff handoff; fair head-to-head restricted to claude/Sonnet.
- Cold-reviewer op-lesson: canonical `review_with_codex.sh` / `codex exec --yolo` flaky (parse-fail then 360s timeout on ~16k-char prompt) — fell back to fresh `general-purpose` Claude subagent (CLAUDE.md tenet 3 allows "codex exec, AO worker, or equivalent"). Subagent's final JSON does NOT surface in foreground Agent return; retrieve via `TaskOutput` on the agentId.

## Key Quotes
> "Result: NO separation on ANY axis at n=10."

> "Honest finding: dispatch path is irrelevant for tasks the model solves first-pass; does NOT generalize to fix-loop tasks (next experiment)."

## Connections
- [[project_2026-06-05_dynamic_fanout_calibration]] — calibration benchmark that proved the ruler isn't blind
- [[feedback_2026-06-05_evidence_review_unscorable_axes]] — /er review of this PR
- [[DarkFactory]] — repo
- [[WorkflowGraphgen]] — the feature
- [[AttractorSpecReview]] — spec review pipeline
- [[ColdReview]] — subagent-based fallback for codex
- [[GuaranteedReviewerNodes]] — terminal reviewer pattern
- [[ModeAvsAPlusB]] — the A-vs-A+B benchmark pattern
- [[TaskOutputRetrieval]] — subagent final-JSON extraction

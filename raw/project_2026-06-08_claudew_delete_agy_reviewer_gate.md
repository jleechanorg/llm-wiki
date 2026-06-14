---
name: claudew-delete-agy-reviewer-gate
description: Deleted claudew/wafer backend; made agy the SHA-bound reviewer gate with claude infra-fallback; gates resolve per-node backend.
metadata: 
  node_type: memory
  type: project
  originSessionId: b7941c4a-7304-45fb-b753-9b0ec13f0a81
---

2026-06-08 session. Three coupled changes in dark-factory (uncommitted on `main`, alongside unrelated WIP):

1. **Deleted `claudew` (wafer/GLM-5.1) backend** — removed from `runner/handlers.py` (codergen + both gate sites, done across two sessions), `runner/__main__.py` `--backend choices` (now `echo,claude,codex,ao,agy`). `grep -rniE 'claudew|wafer|glm-5|localhost:9001' runner/ pipelines/` = clean.

2. **agy reviewer gate + claude fallback** — new shared helpers in `handlers.py` before `_slash_gate`: `_gate_subprocess_args` (agy gets `--add-dir <workdir> --print-timeout <t>s --print`, else claude), `_run_gate_once` (SHA-bind + verdict-parse + classify, records `reviewer_backend`), `_is_gate_infra_failure` (error OR sandbox-unavailable/timed_out/backend_missing), `_resolve_gate_backend` (node.attrs backend wins over ctx.backend), `_execute_gate` (agy → on infra failure run claude with `fallback_used=true,fallback_from=agy`; **real agy fail/partial is kept, never reviewer-shopped**). Both `_slash_gate.handler` and `_run_universal_prompt_gate` route through `_execute_gate`.
   - **Why `_resolve_gate_backend` was needed**: `engine._run_with_retries` calls gate handlers with run-level `ctx`, so gates historically read `ctx.backend` not per-node attr — a stylesheet/explicit `backend=agy` on a gate node was silently ignored. See [[holdout_eval-emulator-infra]] for the related gate-subprocess invariants.

3. **`pipelines/slim/review_pr.dot` evidence node fixed** — was `type="codergen"` (a worker wearing a reviewer label: editable, no SHA binding, no verdict parse). Converted to `type="gate_er"` with explicit `backend="agy"` (kept `class="review"` for color). **Chose explicit attr over model-stylesheet**: review_pr.dot has no stylesheet, and `_codergen` echo-short-circuits on the *resolved* backend, so a stylesheet forcing the cold `review` node to agy would spawn real agy under `--backend echo` and break smoke. `tests/test_slim.py:48-49,82-83` confirm the repo convention = per-node backend wins; echo smoke explicitly pins nodes to echo. Gates instead echo-short-circuit on `ctx.backend`, so `backend=agy` on a gate is smoke-safe with no pin.

**Tests**: 3 agy gate tests added to `tests/test_gates.py` (runs-agy, falls-back-on-infra-failure, real-fail-not-retried) → 13/13 green.

**Verification gotcha**: full `pytest tests/` showed 11 failures, but the failure *set was non-deterministic between runs*. Root cause = 4 **untracked WIP test files** (`test_base_dot.py`, `test_bug_fix_pipeline.py`, `test_gate_red_green.py`, `test_include.py`) from unrelated include/base-dot/bug_fix lane work polluting global handler/registry state → order-dependent breakage in `test_engine`/`test_slim`. Suite excluding those 4 = **229 passed, 1 failed**. The lone failure `test_conformance_score_is_deterministic_mock_surface` fails in isolation, I never touched conformance, and the WIP `parser.py`/`_base.dot` likely break its self_test subprocess — pre-existing/unrelated. Lesson: when a full suite fails noisily, `git status` first — untracked WIP test files can mask a clean change via global-state pollution; run tracked-only or per-file to isolate.

**Open item flagged to operator**: `docs/diagram-color-semantics.md:29` still lists "wafer" as an LLM-layer example; my edit removing it was reverted (harness flagged the restoration as intentional), so left as-is — it's a color-vocab example string, not functional wiring.

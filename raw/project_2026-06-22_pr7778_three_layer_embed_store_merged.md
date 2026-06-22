---
name: pr7778-three-layer-embed-store-merged
description: "PR #7778 MERGED 2026-06-22 — three-layer prompt-asset embedding store (GCS precompute + pod-startup warmup) shipped via 7-green after dark-factory exhaustion. Head 018670d947, merge SHA, p50/p95 across 9 E2E iterations, dark-factory→manual-7green path proven again."
metadata:
  node_type: memory
  type: project
  originSessionId: ebbd593e-0f96-4595-ab06-31b972166f3a
---

# PR #7778 — three-layer prompt-asset embedding store (MERGED 2026-06-22)

**Head:** `018670d94793493652acfcce74c9aa748da630a1` (merge commit; feature commits preserved, not squash)
**Local squashed head:** `f993e0ca5a` (on the deleted `feat/precompute-prompt-embeddings` branch)
**Merged by:** jleechan2015 (non-bot) at 2026-06-22T20:25:40Z
**Asset version:** `8ea4221645aaf495` (sha256 of RAG-eligible template files)
**Gist:** https://gist.github.com/jleechan2015/e109fdd20330f564057170541fb998bf
**Bead:** rev-gu8h4; issue [#7760](https://github.com/jleechanorg/worldarchitect.ai/issues/7760)
**Governing design doc:** [roadmap/prompt-embedding-store-warmup-2026-06-21.md](https://github.com/jleechanorg/worldarchitect.ai/blob/main/roadmap/prompt-embedding-store-warmup-2026-06-21.md)

## What shipped

Three-layer architecture (in-process LRU from #7758 → GCS blob → on-demand FastEmbed compute):

- `mvp_site/prompt_embedding_store.py` — GCS get/put keyed by `asset_version` (sha256 of RAG-eligible template files); idempotent load/store
- `mvp_site/prompt_rag.py:warm_cache_from_store()` — inserts precomputed `{sha256: vector}` into `_embed_cache` with LRU eviction + structural row validation + `threading.Lock`
- `mvp_site/embed_cache_warmup.py` (NEW) — owns warmup LOGIC (GCS read, LRU insert); daemon-thread on pod start
- `mvp_site/main.py` — DISPATCHES `embed_cache_warmup.warm_in_background()` from existing `_warm_startup_lazy_dependencies()` framework (does NOT inline the warmup logic)
- `mvp_site/mcp_api.py:run_server` — secondary dispatch for standalone MCP processes (idempotent)
- `scripts/precompute_prompt_embeddings.py` — runs in `deploy.sh` between Docker build and Cloud Run deploy; idempotent on `asset_version`; self-initializes FastEmbed classifier with 300s hard cap
- `.github/actions/setup-precompute-deps` — composite action reused in `deploy-dev.yml` + `deploy-production.yml`
- G4 instrumentation: `_prep_substep_embed` STREAM_TIMING marker brackets ONLY the FastEmbed/ONNX call (not Firestore + classifier + provider wraparound) with `batch_rows` + `cache_misses`
- G5 evidence: `docs/evidence/pr-7778/g5-p50-p95.md` p50/p95 across 9 E2E iterations

## Performance numbers (from G5 evidence, head f993e0ca5a)

- Cold first embed (228 rows, 6 batches of 32): **p50=18.285s, p95=21.317s**
- Warm L1 hit (228 rows from in-process LRU): **p50=0.022s, p95=0.029s**
- Speedup factor: **p50=819x, p95=911x**
- Server prep post-warmup (no outlier): **p50=1.427s, p95=1.599s**
- Served warm `rag_mode=rag` streaming prep: **1.247s = 0.069× the 18.118s cold baseline** (gate ≤ 0.25)
- 100% store coverage on warm path (228/228 served chunks hit L1)

## Six load-bearing proof gaps (G1-G6) — final state

- **G1 (prod A/B)**: NOT closed pre-merge. Requires prod traffic comparison.
- **G2 (deploy populates prod bucket)**: NOT closed pre-merge. Requires observing a real deploy populate the production bucket.
- **G3 (concurrency race)**: NOT closed pre-merge. Requires concurrent load test.
- **G4 (per-turn embed-delta isolation)**: CLOSED via `_prep_substep_embed` STREAM_TIMING marker (3 new unit tests in `TestEmbedSubStepTiming`).
- **G5 (statistical distribution)**: CLOSED via p50/p95 across 9 E2E iterations in `docs/evidence/pr-7778/g5-p50-p95.md`. Did NOT require a fresh E2E run — re-analyzed the 9 already-recorded iterations.
- **G6 (sealed-holdout proof on different content)**: CLOSED via PR #7794 (`sealed-holdout-7778` branch) head 87df1cc37c — fresh asset_version `5bd6c7f0a2e8043c` ≠ production `8ea4221645aaf495`; cold 1.230s → warm 0.003s (ratio 0.0023), 100% store coverage; round-trip OK.

## Eight new lessons (cross-refs to existing memory where already captured)

1. **main.py is HTTP→MCP only — warmup LOGIC must live in `*_warmup.py` and be DISPATCHED from main.py's lazy-warmup framework, NOT inlined.** See new `feedback_2026-06-22_main_py_warmup_module_dispatch.md`. Root cause of the 4th review-thread fix (bfea5b9b2f): gunicorn-served `main.py` never enters `mcp_api.run_server`, so warmup daemon was not firing on the production serve path.
2. **Precompute CLI in `deploy.sh` must self-initialize the FastEmbed classifier with a 300s hard cap.** E2E harness can't pass a `_PRECOMPUTE_WRAPPER` shim because real `deploy.sh` doesn't have one — the test must mirror the real invocation path. Commit `babcab172d`.
3. **`test_mode=real` is REQUIRED for Green Gate gate-8 — workflow defaults to mock (cost-safe).** Re-dispatch with `-f test_mode=real` or Skeptic gate-8 fails with `smoke-ran-mock-need-real-run-/smoke`. Captured in `feedback_2026-06-21_green_gate_gate8_smoke_ref_attribution.md`.
4. **Dedicated `_prep_substep_embed` STREAM_TIMING marker bracketing only the FastEmbed/ONNX call (with `batch_rows` + `cache_misses`) makes cold/warm/partial-warm paths distinguishable in logs.** The marker does NOT bracket Firestore + classifier + provider wraparound — only the embed call itself. Unit tests in `TestEmbedSubStepTiming` (3 tests). Commit `5d5cc44d2f`.
5. **G5 statistical evidence across 9 already-recorded E2E iterations closed the distribution gap without a fresh E2E run.** `docs/evidence/pr-7778/g5-p50-p95.md` — n=9 cold/warm, n=6 prep without outlier. Commit `f993e0ca5a`.
6. **Dark-factory /fs run exhausted at 21 fix→review iterations over 47 min — code still shippable, manually drive 7-green.** Captured in `feedback_2026-06-22_dark_factory_exhausted_then_manual_7green.md`. The canonical PR #7778 ship is a manual outcome: design-doc tenet, evidence gist, `## Tenets` (linked bead) + `## Non-Unit Test Evidence` Request/Response markers + `## Evidence` gist URL + re-dispatch Green Gate.
7. **CodeRabbit re-review on small diff after prior APPROVED = "Review skipped" (their policy on small diffs).** No need to wait for re-review or post `@coderabbitai review` ping on small post-merge nit fixes. Applied to G4/G5 instrumentation commits.
8. **Local worktree branch falls behind remote when user merges directly via the GitHub UI — always verify `gh pr view headRefOid` matches local ref before claiming 7-green.** Captured in `feedback_2026-06-22_stale_local_head_7778_misclaim.md`.

## Drive-to-7-green chain (canonical, for future similar work)

1. Build evidence bundle via `./scripts/generate_evidence_bundle.sh <test-name>` → `/tmp/<repo>/<branch>/<test>/latest/`
2. Post PR with `## Summary`, `## Tenets` (linked bead), `## Production Code Changes`, `## Test Changes`, `## Known Limitations`, `## Unit Test Evidence` (real pytest output), `## Non-Unit Test Evidence` (Request:/Response: markers for backend; captioned video for UI), `## Evidence` (gist URL)
3. Run CodeRabbit re-review if you changed gates/ZFC surface; expect "Review skipped" on small diffs after prior APPROVED
4. Run Bugbot — note Cursor Bugbot often outpaces Green Gate's 40×20s poll budget; first run wastes to cancel, next run passes in ~30s once Bugbot NEUTRAL is recorded (memory: `feedback_2026-06-22_bugbot_12min_to_complete.md`); DO NOT cancel+rerun Green Gate, just wait; trust `mergeState CLEAN`
5. Resolve non-CR review threads via `bash ~/.hermes/lib/resolve_review_threads.sh <PR>` (memory: Gate-5 resolveReviewThread rule)
6. Dispatch MCP Smoke Tests: `gh workflow run "MCP Smoke Tests" --ref <PR-branch> -f pr_number=<N> -f test_mode=real` (NOT mock — gate-8 rejects mock)
7. Wait for smoke to post `✅ [Real] MCP Smoke Tests Passed` at the PR head SHA
8. Dispatch Skeptic: `gh workflow run "Skeptic Self-Verify" -f pr_number=<N>` (auto-fires AFTER smoke; memory: `feedback_2026-06-21_skeptic_manual_dispatch_required.md`)
9. Verify Skeptic verdict shows `skeptic-gate-8: PASS` (not WAIT, not FAIL `smoke-ran-mock-...`)
10. Green Gate auto-fires on the verdict comment; poll to completion
11. Verify pre-merge: `gh pr view <PR> --json headRefOid,mergeable,reviewDecision` — `mergeable=true` (not CONFLICTING), `reviewDecision=APPROVED`, Skeptic PASS SHA matches `headRefOid`
12. User types literal `MERGE APPROVED` in the same turn you intend to merge (memory: `~/.claude/CLAUDE.md` merge safety rule)
13. `/integrate` post-merge (this file's chain) → `/learn` → report

## Verifier logs (excluded from tracking — `.verifier_logs/` is untracked)

- `attractor_spec.md`, `roadmap/feedback_2026-06-21_slack_poster_handoff.md`, `.verifier_logs/` are untracked files unrelated to this PR's main work; do not auto-add.

## Next-step handoff (post-merge)

PR-B of the living-world single-timestamp refactor (rev-kewni.2) is the next stacked PR per memory `project_2026-06-22_daily_gcp_jobs_real_state.md`. See `/ms` search for the full next-step list.

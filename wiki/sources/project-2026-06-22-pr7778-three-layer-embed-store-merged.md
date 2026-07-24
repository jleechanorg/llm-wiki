---
title: "PR #7778 three-layer prompt-embed store MERGED — drive-to-7-green chain + main.py warmup module pattern"
type: source
tags: [worldarchitect, rag, embeddings, gcs, fastembed, cloud-run, dark-factory, evidence, pr-7778, rev-gu8h4]
date: 2026-06-22
source_file: ../../raw/project_2026-06-22_pr7778_three_layer_embed_store_merged.md
---

## Summary
PR #7778 MERGED 2026-06-22 (head `018670d947`, merge commit by jleechan2015 at 20:25:40Z) shipped the three-layer prompt-asset embedding architecture: in-process LRU (from #7758) → GCS blob → on-demand FastEmbed compute. p50/p95 across 9 E2E iterations: cold first embed p50=18.3s / p95=21.3s vs warm L1 hit p50=22ms / p95=29ms = 819x speedup at p50, 911x at p95. Closed G4 (per-turn embed-delta STREAM_TIMING marker) and G5 (statistical distribution); G1/G2/G3 explicitly out of pre-merge scope. Drive-to-7-green chain after dark-factory exhaustion proven again.

## Key Claims
- Three-layer architecture in-process LRU → GCS blob → compute is a deploy-time precompute + pod-startup warmup pattern that eliminates ~14s FastEmbed cold-start on new Cloud Run pods
- `mvp_site/main.py` is HTTP→MCP only — startup warmup LOGIC must live in a dedicated `mvp_site/<feature>_warmup.py` module and be DISPATCHED from main.py's `_warm_startup_lazy_dependencies()` framework, not inlined
- Bug class: dispatching warmup only from `mcp_api.run_server`'s `__main__` block silently skips it on gunicorn-served main.py (production path). Wiring fix in commit `bfea5b9b2f`
- Precompute CLI in `deploy.sh` must self-initialize the FastEmbed classifier with a 300s hard cap — E2E harness must mirror real `deploy.sh` invocation, no `_PRECOMPUTE_WRAPPER` shim
- G4 instrumentation: dedicated `_prep_substep_embed` STREAM_TIMING marker brackets ONLY the FastEmbed/ONNX call (not Firestore + classifier + provider wraparound), reporting `batch_rows` + `cache_misses` so cold/warm/partial-warm paths are distinguishable
- G5 statistical evidence across already-recorded E2E iterations closes the distribution gap without a fresh E2E run
- Green Gate gate-8 smoke `test_mode` defaults to `mock` (cost-safe) — must dispatch with `-f test_mode=real` or Skeptic gate-8 fails with `smoke-ran-mock-need-real-run-/smoke`
- CodeRabbit re-review on small diff after prior APPROVED = "Review skipped" (their policy on small diffs)
- Local worktree branch falls behind when user merges directly via the GitHub UI — always verify `gh pr view headRefOid` matches local ref before claiming 7-green
- Dark-factory /fs run exhausted at 21 fix→review iterations over 47 min — code still shippable, manually drive 7-green via evidence gist + PR body sections + re-dispatch Green Gate

## Key Quotes
> "main.py may *dispatch* such warmups through its existing `_warm_startup_lazy_dependencies()` framework ... The actual warmup LOGIC (GCS load, LRU insert) lives in the warmup module, not in `main.py`."

> "p50=18.285s, p95=21.317s" (cold first embed) vs "p50=0.022s, p95=0.029s" (warm L1 hit) — 819x/911x speedup

## Connections
- [[MainPyWarmupModuleDispatch]] — the architectural pattern codified in CLAUDE.md and main.py docstring, proven by the bfea5b9b2f wiring fix
- [[ThreeLayerEmbedStore]] — the L1 (in-process LRU) → L2 (GCS) → L3 (compute) architecture
- [[DarkFactoryExhaustedManual7Green]] — the manual 7-green path when dark-factory's test path fails on a quoting/env bug
- [[GCSStoreIdempotentPrecompute]] — the deploy-time precompute → GCS blob pattern (idempotent on asset_version)
- [[StreamingTimingMarker]] — the per-turn instrumentation pattern for cold/warm/partial-warm attribution
- [[GreenGateGate8SmokeRealMode]] — the test_mode=real requirement for gate-8
- [[DriveTo7GreenChain]] — the canonical chain captured for reuse

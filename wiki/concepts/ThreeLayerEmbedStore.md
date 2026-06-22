---
title: "Three-Layer Embed Store (L1 LRU → L2 GCS → L3 compute)"
type: concept
tags: [architecture, worldarchitect, rag, embeddings, gcs, fastembed, pr-7778, pr-7758]
date: 2026-06-22
---

## Summary
The prompt-asset embedding architecture for WorldArchitect.AI's RAG path. Three layers, in order from cheapest to most expensive:
1. **L1 — in-process LRU** (`prompt_rag._embed_cache`): content-hash keyed dict, thread-safe via `threading.Lock`, populated on first lookup and from L2 warmup
2. **L2 — GCS blob** (`prompt_embedding_store.py`): versioned gzip-pickle keyed by `asset_version` (sha256 of RAG-eligible template files); precomputed at deploy time by `scripts/precompute_prompt_embeddings.py`
3. **L3 — on-demand FastEmbed compute**: fallback for cache misses; the only path that writes back to L1 (LRU eviction)

## Why three layers
- L1 alone (PR #7758): 94% prep-time drop on warm pods but in-process cache is pod-local, so new pods paid ~14s FastEmbed cold-start on first RAG/shadow turn
- L1 + L2 (PR #7778): new pods load the GCS blob at startup via `embed_cache_warmup.warm_in_background()` daemon thread; L1 LRU is already warm on the first served turn
- L1 + L2 + L3 fallback: any cache miss at serve time still computes on demand (no L2 reads at serve time, no writes to L2 at serve time); the GCS blob is deploy-time-only

## Performance (p50/p95 across 9 E2E iterations)
- Cold first embed (228 rows, 6 batches of 32): p50=18.285s, p95=21.317s
- Warm L1 hit (228 rows from in-process LRU): p50=0.022s, p95=0.029s
- Speedup factor: p50=819x, p95=911x
- Server prep post-warmup: p50=1.427s, p95=1.599s

## Source
- `mvp_site/prompt_embedding_store.py` (GCS get/put)
- `mvp_site/prompt_rag.py:warm_cache_from_store()` (L1 insertion with LRU eviction)
- `mvp_site/embed_cache_warmup.py` (pod-startup daemon)
- `scripts/precompute_prompt_embeddings.py` (deploy-time precompute)
- `docs/evidence/pr-7778/g5-p50-p95.md` (G5 statistical evidence)
- `roadmap/prompt-embedding-store-warmup-2026-06-21.md` (design doc)

## Related
- [[MainPyWarmupModuleDispatch]] — the warmup dispatch pattern
- [[GCSStoreIdempotentPrecompute]] — the deploy-time precompute pattern
- [[EmbeddingVector]] — the underlying vector representation
- PR [#7758](https://github.com/jleechanorg/worldarchitect.ai/pull/7758) (L1 only)
- PR [#7778](https://github.com/jleechanorg/worldarchitect.ai/pull/7778) (L1+L2+L3)
- Bead rev-gu8h4; issue [#7760](https://github.com/jleechanorg/worldarchitect.ai/issues/7760)

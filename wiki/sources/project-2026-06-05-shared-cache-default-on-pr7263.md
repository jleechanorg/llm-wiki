---
title: "Shared System/Tools Gemini Cache Default-ON (PR #7263)"
type: source
tags: ["gemini-cache", "cost-optimization", "worldarchitect-ai", "pr-7263"]
date: 2026-06-05
source_file: project_2026-06-05_shared_cache_default_on_pr7263.md
---

## Summary
PR #7263 ships Option-2 shared system/tools Gemini cache default-ON, gated to real multi-turn play by skipping test traffic. Proof split: gate-independent A/B engagement (74.6% input-token reduction) + testing_mcp correct-skip evidence.

## Key Claims
- Shared cache default-ON at `mvp_site/gemini_shared_cache.py:60`, module constant, NO env var
- Routing helper `llm_service._should_use_shared_cache(user_id)` mirrors `_should_use_explicit_cache` and wraps all THREE engagement points (non-streaming, deferral driver, streaming gate)
- 74.6% input-token reduction proven via `scripts/shared_cache_ab.py` direct real Gemini SDK
- Test traffic (~89% of historical Gemini volume) skipped — one-shot fixtures get ~0 cross-turn reuse
- Pushed baeedefb68; PR MERGEABLE, headRefOid baeedefb68, reviewDecision EMPTY (fresh CodeRabbit pending)

## Key Quotes
> no make it default on and test it — chosen scope On + skip test traffic — cache engages only for real multi-turn play

> 74.6% input-token reduction, single `cachedContents/...` reused both calls, cached_tokens 30829 (99.5%/99.4%)

## Connections
- [[AgentOrchestrator]] — related to self-hosted runner pool expansion
- [[GeminiCache]] — cache strategy concept
- [[BigQueryBilling]] — re-prove savings post-merge

---
title: "Shared System/Tools-Only Gemini Cache SPIKE — Verdict GO"
type: source
tags: ["gemini-cache", "spike", "worldarchitect-ai", "pr-7259", "cost-optimization"]
date: 2026-06-04
source_file: project_2026-06-04_shared_system_tools_cache_spike_go.md
---

## Summary
Shared system/tools-only explicit cache SPIKE resolved with verdict GO. D1 (real paid Gemini): 99.8% static floor discount on read. A2 (synthetic): byte-identical payloads, zero leakage. D2 cost: Option 2 = −74%/call, Option 1 = −61% fallback. Storage collapses O(campaigns)=$1,440/day → O(~6 caches)=$8.64/day.

## Key Claims
- D1: campaign-free system+tools-only explicit cache discounts 99.8% of static floor on read (cached=8580/prompt=8594)
- C3: referencing cache + setting system_instruction/tools → HTTP 400 (system must move fully into cache)
- C1: `cached_content` is single Optional[str] — one cache per request (two-cache design NOT constructible)
- A2: byte-identical payload sha256=bde3c4955afef0cc536dc306113d01c916b6fa21b1cde5526de92828c9c33d88 (1 distinct digest, 45577 bytes)
- Storage: $1,440/day → $8.64/day (O(~6 caches))
- Spike PR #7259 OPEN/NOT merged; defer to impl bead rev-n6nbs.1

## Key Quotes
> D3 verdict: GO — to the follow-up IMPLEMENTATION bead rev-n6nbs.1, NOT to merge the spike. Option 2 primary, Option 1 fallback

## Connections
- [[GeminiCache]] — concept
- [[BigQueryBilling]] — savings proof

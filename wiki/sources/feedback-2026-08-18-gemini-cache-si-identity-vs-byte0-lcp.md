---
title: "Gemini implicit cache — SI identity vs byte-0 JSON LCP"
type: source
tags: [gemini, implicit-cache, pr-8856, latency, forensics]
date: 2026-08-18
last_updated: 2026-08-18
source_file: raw/feedback_2026-08-18_gemini_cache_si_vs_byte0_lcp.md
sources:
  - raw/feedback_2026-08-18_gemini_cache_si_vs_byte0_lcp.md
---

## Summary

Live 2026-08-18 httpx forensics on nocturne campaign `SGxsM2xdermqwOmI37SF` showed [PR 8856](https://github.com/jleechanorg/worldarchitect.ai/pull/8856) achieved same-agent `systemInstruction` byte identity while the raw Gemini HTTP body still shares only 8–12% from byte 0. The SDK serializes `contents` first; story compaction rewrites early history. `cached_tokens` match SI-first tokenization, not JSON key order.

## Key Claims

- Same-agent SI→EOF SHA was 100% stable per agent on this campaign.
- Same-agent raw-body LCP from byte 0 was 8–12%; first diff sat in compacted `story_history`.
- JSON-order LCP predicted ~32k cached tokens; observed 138,697. Duplicate Rewards 11s later: 98.1%.
- `STREAM_CACHE_USAGE source=not_used` means explicit cache off, not implicit miss.
- Pooled implicit hit rate did not rise after 8856. Bible dedup (`rev-fl4z6`) is still a plan, not shipped.

## Key Quotes

> "Do not treat contents-first JSON as proven Gemini cache-prefix bug."

> "Measure both (1) same-agent SI identity and (2) byte-0 LCP of authoritative gemini_httpx_send bodies, then compare predicted tokens from each LCP against cached_tokens."

## Connections

- [[GeminiImplicitCachePrefixMeasurement]] — the two-LCP + cached_tokens discriminator
- [[CampaignBibleDuplication]] — remaining latency lever (~300k prompt tokens)
- [PR #8856](https://github.com/jleechanorg/worldarchitect.ai/pull/8856) — SI stability merge
- [Issue #9059](https://github.com/jleechanorg/worldarchitect.ai/issues/9059) — nocturne latency REPRO

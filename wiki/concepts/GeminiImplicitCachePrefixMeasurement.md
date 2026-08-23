---
title: "Gemini implicit-cache prefix measurement"
type: concept
tags: [gemini, cache, measurement]
date: 2026-08-18
last_updated: 2026-08-18
---

# GeminiImplicitCachePrefixMeasurement

Gemini implicit caching is longest-common-prefix over the **tokenized** request, not necessarily over the HTTP JSON bytes.

## Two LCPs to report

1. **SI identity** — SHA256 of the `systemInstruction` slice (from `"systemInstruction"` to EOF, or parsed parts[0].text). This is what [PR 8856](https://github.com/jleechanorg/worldarchitect.ai/pull/8856) optimized.
2. **Byte-0 body LCP** — longest common prefix of consecutive same-agent authoritative `gemini_httpx_send` `request_json` strings. On 2026-08-18 nocturne this was 8–12% because live JSON is contents-first.

## Discriminator

Convert each LCP from chars to tokens (~3.9 JSON chars/token on those rows) and compare to `cached_tokens`. If JSON-order LCP under-predicts cache by a large factor, the tokenizer is not using JSON key order (observed: 32k predicted vs 139k cached; SI-sized hits ~50%; 98% when contents also matched).

## Anti-patterns

- Treating `STREAM_CACHE_USAGE source=not_used` as an implicit miss (that flag is explicit cache).
- Treating SI-first test fixtures as the live wire.
- Writing a planned payload-dedup as already restoring >75% cache.
- Reordering JSON keys as the latency fix without the discriminator above.

See [[feedback-2026-08-18-gemini-cache-si-identity-vs-byte0-lcp]].

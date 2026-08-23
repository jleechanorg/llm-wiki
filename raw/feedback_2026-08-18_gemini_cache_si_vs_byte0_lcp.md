---
name: Gemini implicit cache — SI identity vs byte-0 JSON LCP
description: Same-agent systemInstruction can be 100% stable while raw HTTP LCP from byte 0 is only ~10%; cached_tokens discriminate tokenizer order from JSON key order.
type: feedback
bead: rev-6653w
---

On 2026-08-18 live httpx bodies for campaign `SGxsM2xdermqwOmI37SF`, Gemini REST JSON is **contents-first** (`{"contents":...` at byte 2, `systemInstruction` at ~637k–702k). [PR #8856](https://github.com/jleechanorg/worldarchitect.ai/pull/8856) evidence fixtures assume SI-first JSON.

**Measured:**

- Same-agent SI→EOF SHA: 100% identical (Rewards `b2ebb1b3…`, Story `dfb018de…`).
- Same-agent raw-body LCP from byte 0: **8–12%** (first diff in compacted `story_history`).
- JSON-order LCP of 128,137 chars predicts ~32k cached tokens; observed **138,697**. Duplicate call 11s later: **98.1%** cached.
- Pooled implicit hit rate did **not** rise after 8856 (dev 62.3% → 43.1% → 47.2%). STREAM_CACHE_USAGE `not_used` is **explicit** cache off, not implicit miss.

**Why:** Gemini’s `cached_tokens` match SI-first proto tokenization plus extra contents when the contents prefix also matches. JSON key order is a fixture/measurement trap, not proven tokenizer order.

**How to apply:** For any implicit-cache claim, report **both** (1) same-agent SI identity and (2) byte-0 LCP of authoritative `gemini_httpx_send` bodies, then compare predicted tokens from each LCP against `cached_tokens`. Do not treat planned bible-dedup or 0% cache as shipped. Do not reorder JSON keys as the latency fix without that discriminator.

**Verification:** `/tmp/worldarchitect.ai/latency-SGxsM2xdermqwOmI37SF/lcp/8856-lcp-verdict.md`. Beads: `rev-53zwf`, `rev-mkgy6`, `rev-m48hx`, `rev-6653w`.

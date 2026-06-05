# Shared System/Tools-Only Gemini Cache — Measured Spike (GO verdict)

- **Raw source:** `~/llm_wiki/raw/learnings/shared-system-tools-cache-spike-2026-06-04.md`
- **md5:** `7c65e274987238938558366e0eec037a` (32 lines)
- **Origin:** Claude auto-memory `project_2026-06-04_shared_system_tools_cache_spike_go.md`, derived from spike `spec/feature.md` (canonical; BigQuery is reconciliation-only, NOT display-name attribution).
- **Ingested:** 2026-06-04
- **Why this matters:** Resolves the cache-redesign question teed up by the [[GeminiContextCacheTTL]] prefix-stability audit. Proves a campaign-free, shared, system/tools-only explicit cache is constructible, safe, and the cheapest option for the floor-dominated test/CI traffic that is 89% of [[GeminiCostApportionment]] spend (epic `rev-9piwk`).

## Finding

- **D1 (real paid Gemini):** system+tools-only explicit cache discounts **99.8% of the static floor on read** (`cached_content_token_count=8580` / `prompt_token_count=8594`).
- **C3:** referencing a cache while ALSO setting `system_instruction`/`tools` → **HTTP 400**. System must move fully into the cache.
- **C1:** `cached_content` is a single `Optional[str]` — one cache per request (two-cache design impossible).
- **A2 (synthetic safety proof, no key):** two distinct contexts (camp-alpha/user-1/Itachi vs camp-beta/user-2/Gandalf) build a **BYTE-IDENTICAL** payload, `sha256=bde3c4955afef0cc536dc306113d01c916b6fa21b1cde5526de92828c9c33d88`, 1 digest, 45577 bytes, zero leakage. This byte-identity is the impl regression invariant.
- **A4:** shared-cache key = **(model, system_prompt_sha256, tool_signature_sha256)**; `response_schema` not a key dimension.
- **D2 cost model:** Option 2 (shared explicit system/tools cache) = **−74%/call** ($5.36e-3 vs $2.05e-2); Option 1 (implicit + contiguous-floor reorder) = **−61% fallback**. Storage **O(campaigns)=$1,440/day → O(~6 caches)=$8.64/day**.
- **D3 verdict: GO** → impl bead `rev-n6nbs.1` (parent `rev-n6nbs`, epic `rev-9piwk`), **not** merge of the spike. Constraint C8: spike did NOT reorder `finalize_instructions()`/llm_service request path. Deferred A3a (settled BQ window via dev-runner SA) + A3c (real-path A/B Options 0/1/2) gate defaulting Option 2 ON.

## References

- PR: https://github.com/jleechanorg/worldarchitect.ai/pull/7259 (branch `spike/shared-system-tools-cache`, HEAD `69311f04b4`, OPEN, human merge gate)
- Concepts: [[GeminiContextCacheTTL]], [[GeminiCostApportionment]], [[CachedSystemInstructionTokens]]
- Bead: `rev-n6nbs.1` (new child impl bead)

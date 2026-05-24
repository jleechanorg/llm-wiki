# Gemini API Cost Investigation 2026-05-24

**Ingested**: 2026-05-24
**Raw**: [gemini-cost-investigation-2026-05-24.md](../../raw/gemini-cost-investigation-2026-05-24.md)
**Project**: worldarchitect.ai (`worldarchitecture-ai` GCP)

## Summary

Root-caused $85/day Gemini API charges. Context cache **storage** dominates at 78% ($66/day), driven by 1-hour TTL causing continuous cache-create churn. CI is free via SMOKE_TOKEN mock mode. Dev server is #1 cost driver (129 calls/day).

## Key findings

- Cache storage = ~20 creates/hr × 165K tokens × $1/1M tokens/hr × 24hr = ~$66/day
- Cache-miss full re-input = ~$14/day (sessions resuming after TTL expiry)
- Fix: PR #7074 extends TTL 1hr→4hr → expected ~$50/day savings
- Fix: PR #7066 MERGED — test cache default read_write (59% CI token reduction)
- `STREAM_CACHE_USAGE source=created` log label = billed event identifier
- SMOKE_TOKEN activates mock mode on Cloud Run servers → zero Gemini billing from CI

## Concepts

- [[GeminiContextCacheTTL]] — new concept page needed
- [[CachedSystemInstructionTokens]] — related (system instruction cache overhead)

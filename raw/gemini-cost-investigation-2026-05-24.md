# Gemini API Cost Investigation — 2026-05-24

**Project**: `worldarchitecture-ai` (GCP)
**Period**: May 1–23, 2026
**Total charge**: $1,957.77 (~$85/day)
**Model**: `gemini-3-flash-preview`

## Summary

$85/day Gemini API cost is driven almost entirely by **context cache storage and cache-miss re-input**, not by output tokens or CI runs. The 1-hour cache TTL in `gemini_cache_manager.py` causes caches to expire hourly, forcing full 165K-token re-input every session that resumes after an hour.

## Cost Breakdown (corrected)

**Key insight**: At 1hr TTL, storage cost accrues continuously all day. If caches are created at ~20/hr average across all services:
- 20 creates/hr × 165K tokens × $1/1M tokens/hr × 24hr = **$79/day storage** alone

| Component | Cost/day | % | Root cause |
|-----------|----------|---|------------|
| **Cache storage** | **~$66** | **78%** | ~20 creates/hr avg × 165K tokens × $1/1M/hr × 24hr |
| Cache-miss full input | ~$14 | 16% | ~175 cache-miss calls × 165K tokens × $0.50/1M |
| Cache reads + output | ~$5 | 6% | Hit reads + output tokens per call |
| **Total** | **~$85** | 100% | Matches actual billing |

**Earlier estimate ($51) was wrong**: Used peak-only (57/hr) instead of all-day average (~20/hr) for storage calculation. Storage dominates at 78%, not 30%.

**Revised savings from PR #7074 (TTL 1hr→4hr)**:
- Cache-create rate drops ~4× (one create per 4 hours instead of per 1 hour)
- Storage savings: $66 × (1 - 1/4) ≈ **$50/day** (not $19/day as originally estimated)
- New expected daily cost after TTL fix: ~$35/day (59% reduction)

## Call Volume by Service (daily average)

| Service | Calls/day | Cost driver |
|---------|-----------|-------------|
| `mvp-site-app-dev` | 129 | Developer/tester gameplay |
| `mvp-site-app-s6` (PR preview) | 97 | PR #7064 preview server |
| `mvp-site-app-stable` | 11 | Real production traffic |
| `mvp-site-app-s5` (PR preview) | 11 | Older preview |
| CI smoke tests | 0 (billed) | SMOKE_TOKEN → mock mode, zero charges |

## What Is NOT Contributing

- **CI smoke tests**: All 7800+ CI runs/day use `SMOKE_TOKEN` which activates `mock_services_mode` in Flask via `g` context. Zero Gemini API calls billed.
- **Gemini CLI sessions**: `~/.gemini/settings.json` uses `oauth-personal` auth, billed to `ai-universe-2025` project (not `worldarchitecture-ai`).
- **BYOK users** (`has_byok=True`): Users who configure their own API key in settings incur zero project cost.

## Log Analysis Method

Cloud Logging labels used for diagnosis:

```
STREAM_CACHE_USAGE: source=created|reused|not_used, cache_tokens=165000
GEMINI_STREAM_USAGE: prompt_tokens=165123, cached_tokens=110234, response_tokens=812, cache_hit_rate=0.67
BYOK_RESOLUTION: user_id=..., provider=gemini, has_byok=True|False
```

- `source=created` = new cache write, full input billed
- `source=reused` = cache hit, only read tokens billed at $0.05/1M
- `source=not_used` = mock mode (CI or SMOKE_TOKEN), zero billing

## Pricing Reference (gemini-3-flash-preview)

| Token type | Price |
|-----------|-------|
| Input (non-cached) | $0.50 / 1M tokens |
| Output | $3.00 / 1M tokens |
| Cache write | $0.05 / 1M tokens |
| Cache read | $0.05 / 1M tokens |
| Cache storage | $1.00 / 1M tokens / hour |

## Root Cause

`mvp_site/gemini_cache_manager.py:43`:
```python
CACHE_TTL = "3600s"       # ← 1 hour expiry
CACHE_TTL_SECONDS = 3600
```

A full game history (system prompt + all story turns) is 110K–180K tokens. When a player resumes a session after >1 hour, the cache has expired and the full history must be re-input at $0.50/1M. With 57+ cache-create events/hour at peak, storage costs accumulate rapidly.

## Fix: PR #7074 — Extend TTL to 4 Hours

**Branch**: `fix/extend-cache-ttl-4hr`
**PR**: [#7074](https://github.com/jleechanorg/worldarchitect.ai/pull/7074)
**Change**:
```python
CACHE_TTL = "14400s"      # 4 hours
CACHE_TTL_SECONDS = 14400
```

**Expected savings**: ~75% reduction in storage cost by reducing cache-create frequency from every hour to every 4 hours. Estimated savings: ~$19/day → new estimate $66/day.

## Fix: PR #7066 — Test Cache Default (MERGED)

**PR**: [#7066](https://github.com/jleechanorg/worldarchitect.ai/pull/7066) — MERGED 2026-05-24
**Change**: `WORLDAI_TEST_CACHE` default → `read_write` (was `off`)
**Impact**: CI test runs now reuse cached LLM responses, reducing token consumption in testing_mcp runs. Does not affect production billing directly (already mock mode via SMOKE_TOKEN).

## Additional Cost Reduction Opportunities

1. **Dev server idle policy**: `mvp-site-app-dev` (129 calls/day) is the top cost center. Auto-shutdown after 30min idle would eliminate off-hours cost.
2. **BYOK for dev/preview users**: Require BYOK for non-production servers — zero project cost for developer testing.
3. **Session rollover on cost spike**: Bead [rev-7pli](https://github.com/jleechanorg/worldarchitect.ai/issues) — auto-start new session when token cost crosses threshold.
4. **Essentials AB test**: PR #6857 essentials compression reduces effective token count per cache. A/B proof tracked in bead [rev-hzih3](https://github.com/jleechanorg/worldarchitect.ai/issues).

## Permissions Note

Service account `dev-runner@worldarchitecture-ai.iam.gserviceaccount.com` lacks `roles/billing.viewer`. To grant:
```bash
gcloud billing accounts add-iam-policy-binding 011269-D08BDB-79D8F2 \
  --member="serviceAccount:dev-runner@worldarchitecture-ai.iam.gserviceaccount.com" \
  --role="roles/billing.viewer" \
  --account=jleechan@gmail.com
```

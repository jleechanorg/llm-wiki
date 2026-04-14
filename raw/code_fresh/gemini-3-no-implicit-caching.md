# Gemini 3 Implicit Caching Support - Research Findings

**Created**: 2026-01-23
**Status**: ✅ Research Complete
**Priority**: High - Cost Optimization Impact
**Finding**: **Gemini 3 DOES support implicit caching**

## Research Summary

### ✅ CONFIRMED: Gemini 3 Has Implicit Caching

Official documentation confirms **all Gemini 3 models support implicit caching**:

**Source**: [Context caching | Gemini API](https://ai.google.dev/gemini-api/docs/caching)

**Supported Models with Minimum Token Requirements**:
- `gemini-3-flash-preview`: 1,024 tokens minimum
- `gemini-3-pro-preview`: 4,096 tokens minimum
- `gemini-2-5-flash`: 1,024 tokens minimum
- `gemini-2-5-pro`: 4,096 tokens minimum

## Key Differences Between Gemini 2.5 and 3.0

### Discount Rates

**Gemini 2.5 Models**:
- Implicit caching: 75% discount (announced May 8, 2025)
- Explicit caching: 90% discount
- Source: [Gemini 2.5 Models now support implicit caching](https://developers.googleblog.com/en/gemini-2-5-models-now-support-implicit-caching/)

**Gemini 3 Models**:
- Implicit caching: 90% discount (improved from 2.5)
- Explicit caching: 90% discount
- Source: Web search results (multiple sources confirm 90% for Gemini 3)

### Why Our Logs Show 0% Cache Hit

**The Issue**: We're using `gemini-3-flash-preview` but getting `cached_tokens=0`

**Possible Reasons**:

1. **Request Size Below Minimum** (UNLIKELY)
   - Our request: 233,255 tokens
   - Minimum required: 1,024 tokens
   - ✅ We exceed the minimum by far

2. **No Matching Prefix** (LIKELY)
   - First request after field reordering deployment
   - No previous requests with new field order
   - Cache needs multiple requests with same prefix to hit

3. **Model Selection Issue** (POSSIBLE)
   - Forum report: [Implicit Context Caching does not work with Gemini 3 Pro Preview](https://discuss.ai.google.dev/t/implicit-context-caching-does-not-work-with-gemini-3-pro-preview/111253)
   - User reports caching stopped working for Gemini 3 Pro
   - Threshold changed from 2048 to 4096 without notice
   - Some users migrating to competitors due to caching issues

4. **Preview Model Limitations** (POSSIBLE)
   - `-preview` models might have different behavior
   - Production models might have more reliable caching
   - Documentation focuses on stable releases

## What We Should See Next

**Expected Behavior After Field Reordering**:

1. **First request**: `cached_tokens=0` (no previous cache)
2. **Second request**: `cached_tokens=0` (building cache)
3. **Third+ requests**: `cached_tokens>0` (70-90% hit rate expected)

**Expected Cache Hit Rate**:
- Gemini 3: 90% discount on cached tokens
- With 233K token requests and ~31K story history
- Expected: 150K-170K tokens cached
- Cost reduction: 60-70% overall

## Recommendations

### Short-term (Immediate)

1. **Monitor Next Requests**
   - Check if cache hits appear on subsequent requests
   - Look for GEMINI_USAGE logs with cached_tokens > 0
   - Verify field reordering is working

2. **Switch to Gemini 2.5 if Issues Persist**
   - More stable caching behavior reported
   - 75% discount vs 90% difference is small
   - Better documented and tested

### Long-term (Strategic)

1. **Consider Explicit Caching**
   - Guaranteed 90% discount
   - More control over cache behavior
   - TTL management
   - Storage costs to evaluate

2. **Model Selection Strategy**
   - Gemini 3 Flash: Frontier intelligence, 90% caching discount
   - Gemini 2.5 Flash: More stable, 75% caching discount
   - Trade-off: cutting-edge features vs reliability

## Evidence from Research

**Official Sources**:
1. [Context caching | Gemini API](https://ai.google.dev/gemini-api/docs/caching) - Official model support
2. [Gemini 3 Developer Guide](https://ai.google.dev/gemini-api/docs/gemini-3) - Confirms caching support
3. [Gemini 2.5 implicit caching announcement](https://developers.googleblog.com/en/gemini-2-5-models-now-support-implicit-caching/) - 75% discount for 2.5

**Community Reports**:
- [Forum issue: Gemini 3 Pro caching problems](https://discuss.ai.google.dev/t/implicit-context-caching-does-not-work-with-gemini-3-pro-preview/111253) - Ongoing complaints

## Conclusion

**Original Belief**: ❌ "Gemini 3 doesn't support implicit caching"
**Research Finding**: ✅ "Gemini 3 DOES support implicit caching with 90% discount"

**Why We Saw 0% Cache**:
- First request after deployment (no previous cache to hit)
- Need 2-3 requests to build cache
- Preview model may have reliability issues (per forum reports)

**Action Items**:
1. ⏳ Wait for next request and check for cache hits
2. 🔍 Monitor GEMINI_USAGE logs for cached_tokens > 0
3. 🚨 If issues persist, consider Gemini 2.5 Flash fallback
4. 📊 Track cache hit rate over next 24 hours

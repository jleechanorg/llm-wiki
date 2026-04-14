# Log Gemini Raw Response Structure

**Created**: 2026-01-22
**Status**: ✅ Complete
**Priority**: Medium - Debugging & Cache Verification
**Bead ID**: BEAD-u8z

## Problem Statement

Currently, `mvp_site/llm_service.py` only logs:
- First 500 chars of response text: `raw_response_text[:500]`
- Usage metadata: prompt_tokens, cached_tokens, response_tokens, cache_hit_rate

We're missing structured logging of the full Gemini response object, which contains:
- Response structure metadata
- Candidates and safety ratings
- Full parts structure
- Finish reasons
- Other diagnostic information

This limits our ability to:
- Debug caching behavior comprehensively
- Understand response structure issues
- Diagnose safety filtering or finish reason problems
- Verify implicit caching is working correctly across all response fields

## Current Logging

**Line 1181** (`_parse_and_validate_response`):
```python
logging_util.debug(f"[{context}] Raw Gemini response: {raw_response_text[:500]}...")
```

**Lines 1574-1601** (`_call_llm_api`):
```python
# Log usage metadata for implicit caching verification (Gemini only)
if hasattr(response, 'usage_metadata'):
    usage = response.usage_metadata
    # ... logs prompt_tokens, cached_tokens, response_tokens, cache_hit_rate
```

## Desired Logging

Add structured logging of full response object after usage_metadata logging:

```python
# Log full response structure for debugging (Gemini only)
if hasattr(response, 'candidates'):
    response_summary = {
        'candidate_count': len(response.candidates) if response.candidates else 0,
        'finish_reason': getattr(response.candidates[0], 'finish_reason', None) if response.candidates else None,
        'safety_ratings': [
            {
                'category': str(rating.category),
                'probability': str(rating.probability)
            }
            for rating in getattr(response.candidates[0], 'safety_ratings', [])
        ] if response.candidates else [],
        'parts_count': len(response.candidates[0].content.parts) if response.candidates and hasattr(response.candidates[0], 'content') else 0,
        'text_length': len(response.text) if hasattr(response, 'text') else 0,
    }

    logging_util.info(
        f"🔍 GEMINI_RESPONSE_STRUCTURE: "
        f"candidates={response_summary['candidate_count']}, "
        f"finish_reason={response_summary['finish_reason']}, "
        f"parts={response_summary['parts_count']}, "
        f"text_len={response_summary['text_length']}, "
        f"safety_ratings={len(response_summary['safety_ratings'])}"
    )
```

## Implementation Plan

1. ✅ Create bead documenting the task
2. ✅ Add response structure logging after usage_metadata (line ~1601)
3. ✅ Add defensive handling for missing attributes (use getattr with defaults)
4. ✅ Test with mock responses to ensure no crashes
5. ⏳ Deploy and verify GCP logs show structured response info (pending PR merge)

## Expected Benefits

- **Better debugging**: See full response structure, not just text preview
- **Cache verification**: Understand if caching affects response structure
- **Safety filtering**: Quickly identify if responses are being filtered
- **Finish reasons**: Diagnose incomplete responses (STOP, MAX_TOKENS, SAFETY, etc.)
- **Response quality**: Track when responses have unusual structure

## Testing Approach

1. Run existing tests to ensure logging doesn't break functionality
2. Check that mock responses work correctly
3. Verify real Gemini responses log all expected fields
4. Confirm GCP logs are parseable and useful

## Implementation Summary

**Commit**: 8a863adec
**PR**: #3963 (added to existing PR with field ordering optimization)

**Changes Made**:

1. **Response Structure Logging** (mvp_site/llm_service.py:1603-1633)
   - Added GEMINI_RESPONSE_STRUCTURE log line after GEMINI_USAGE
   - Logs: candidates, finish_reason, parts, text_len, safety ratings
   - Defensive attribute access with try/except to prevent crashes
   - Works with both real Gemini responses and MagicMock test objects

2. **Enhanced Text Preview Logging** (mvp_site/llm_service.py:1181-1187)
   - Now shows full text length: "Raw response text (2847 chars): ..."
   - Better distinction: this logs extracted text, not full response object

**Example Log Output**:
```
🔍 GEMINI_USAGE: prompt_tokens=230197, cached_tokens=172648, response_tokens=1234, cache_hit_rate=75.0%, model=gemini-2-5-flash-preview
🔍 GEMINI_RESPONSE_STRUCTURE: candidates=1, finish_reason=STOP, parts=1, text_len=2847, safety=HARM_CATEGORY_HATE_SPEECH:NEGLIGIBLE
```

**Testing**:
- All 6 test_gemini_usage_metadata_logging.py tests pass
- Mock objects handled correctly (MagicMock.finish_reason shown in test logs)
- No crashes or errors with missing attributes

## Related Beads

- `.beads/gemini-implicit-caching-verification.md` - Parent bead for caching investigation
- `.beads/optimize-prompt-order-for-caching.md` - Field ordering optimization (PR #3963)

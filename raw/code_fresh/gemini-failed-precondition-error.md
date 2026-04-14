# Gemini FAILED_PRECONDITION Error Investigation

**Created**: 2026-01-23
**Status**: Investigation Required
**Priority**: High - Blocking User Requests
**Error Type**: `400 FAILED_PRECONDITION`

## Problem Statement

Users seeing "sorry system error occurred" message in UI. GCP logs show:

```python
google.genai.errors.ClientError: 400 FAILED_PRECONDITION
{'error': {'code': 400, 'message': 'Precondition check failed.', 'status': 'FAILED_PRECONDITION'}}
```

**Location**: `mvp_site/llm_providers/gemini_provider.py:376` in `generate_json_mode_content`
**Timestamp**: 2026-01-23 03:49:19 UTC
**Campaign**: JXXNfJpdqNtH60HN942q
**Model**: gemini-3-flash-preview
**Request Size**: 233,255 tokens

## Error Traceback

```
File "/app/mvp_site/llm_service.py", line 3726, in continue_story
    api_response = _call_llm_api_with_llm_request(
File "/app/mvp_site/llm_service.py", line 1425, in _call_llm_api_with_llm_request
    return _call_llm_api(
File "/app/mvp_site/llm_service.py", line 1550, in _call_llm_api
    response = gemini_provider.generate_content_with_code_execution(
File "/app/mvp_site/llm_providers/gemini_provider.py", line 791, in generate_content_with_code_execution
    response_1 = phase1()
File "/app/mvp_site/llm_providers/gemini_provider.py", line 769, in phase1
    return generate_json_mode_content(
File "/app/mvp_site/llm_providers/gemini_provider.py", line 376, in generate_json_mode_content
    return client.models.generate_content(
```

## Timing Context

- **Successful request**: 2026-01-23 03:47:39 UTC (completed in 33.61s)
- **Failed request**: 2026-01-23 03:49:19 UTC (2 minutes later)
- Same campaign, same model

## Possible Root Causes

### 1. Field Reordering Impact
**Status**: Under Investigation
- PR #3963 changed LLMRequest field ordering
- First commit (GEMINI_USAGE logging) IS deployed
- Field reordering IS deployed (commit 6baaa697e)
- Could JSON structure change have triggered validation failure?

### 2. Request Size Limits
**Status**: Likely
- Request: 233,255 tokens
- Gemini 3 Flash has 1M context window
- But may have undocumented precondition checks for request structure

### 3. Code Execution Mode Constraints
**Status**: Possible
- Error occurs in `generate_content_with_code_execution`
- Gemini 3 Flash may have different constraints than 2.5 models
- Code execution + JSON mode combination might have limits

### 4. Rate Limiting or Quota
**Status**: Unlikely
- Error is 400 (client error), not 429 (rate limit)
- Successful request just 2 minutes before

### 5. Invalid JSON Structure
**Status**: Possible
- Field reordering might have created unexpected ordering
- JSON schema validation might be order-sensitive
- Python dict insertion order is preserved, but API might expect specific order

## Investigation Steps

1. [x] Check if error is consistent or intermittent - INTERMITTENT (8 errors over 3 hours)
2. [ ] Test with original field ordering (revert PR #3963) - NOT NEEDED (errors pre-date deployment)
3. [x] Check Gemini API changelog for recent changes - No FAILED_PRECONDITION mentions
4. [ ] Verify JSON payload structure is valid
5. [ ] Test with smaller request size to rule out size limits
6. [ ] Check if code_execution mode has specific constraints
7. [x] **DONE**: Add enhanced error logging to capture detailed error information (commit c4e290894)

## Temporary Mitigation

Options:
1. Rollback PR #3963 if field reordering is causing issues
2. Add retry logic with exponential backoff
3. Add request size validation before API call
4. Switch to Gemini 2.5 models (have better caching anyway)

## Related Issues

- PR #3963: Field reordering optimization
- BEAD: optimize-prompt-order-for-caching.md
- User report: "sorry system error occurred" in UI
- Model selection: Using gemini-3-flash-preview (no implicit caching)

## Enhanced Error Logging Solution

**Implemented**: commit c4e290894 (2026-01-23)

Added comprehensive ClientError logging to extract detailed error information:

**What We Now Log**:
1. Basic error attributes (code, status, message)
2. Full error JSON response (pretty-printed)
3. Nested error details with:
   - `@type`: Error type identifier
   - `reason`: Specific failure reason (e.g., TOKEN_LIMIT_EXCEEDED)
   - `domain`: API domain

**Log Format**:
```
🔍 GEMINI_CLIENT_ERROR_DETAILS: code=400, status=FAILED_PRECONDITION, message=...
🔍 GEMINI_ERROR_FULL_JSON: {detailed JSON}
🔍 GEMINI_ERROR_NESTED_DETAILS: N detail(s) found
🔍 GEMINI_ERROR_DETAIL[0]: type=..., reason=..., domain=...
```

**Next Steps**:
1. Wait for next FAILED_PRECONDITION error in production
2. Check logs for detailed error information
3. Identify specific precondition that failed
4. Implement targeted fix based on root cause

**Related Bead**: `.beads/enhance-gemini-error-logging.md`

## Expected Resolution

- ✅ Enhanced error logging deployed (commit c4e290894)
- ⏳ Waiting for next error occurrence to capture details
- Target: Identify root cause within 24 hours of next error
- Deploy fix within 48 hours of root cause identification
- Improve user-facing error messages based on specific error type

# Enhance Gemini Error Logging for FAILED_PRECONDITION

**Created**: 2026-01-23
**Status**: Solution Ready
**Priority**: High - Debugging Production Issues
**Related**: gemini-failed-precondition-error.md

## Problem

Current error handling in `mvp_site/llm_service.py` (lines 1689-1717) only logs `str(e)` which gives:
```
google.genai.errors.ClientError: 400 FAILED_PRECONDITION. {'error': {'code': 400, 'message': 'Precondition check failed.', 'status': 'FAILED_PRECONDITION'}}
```

This is **not detailed enough** - we're missing:
- The `.details` attribute which contains the full response JSON
- Additional error information that might explain WHICH precondition failed
- Token count information if the error is due to token limits
- Any nested error details or field violations

## Research Findings

### ClientError Class Structure

From [googleapis/python-genai/errors.py](https://github.com/googleapis/python-genai/blob/main/google/genai/errors.py):

```python
class ClientError(APIError):
    """Client error raised by the GenAI API."""
    pass

class APIError(Exception):
    # Attributes:
    # - code: HTTP status code (integer)
    # - response: The original response object
    # - status: HTTP status text (string)
    # - message: Error message from response
    # - details: The full response JSON body (dictionary) ← WE NEED THIS!
```

### Common FAILED_PRECONDITION Meanings

From [Vertex AI API errors documentation](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-reference/api-errors):
- Request exceeds model's input token limit
- Model requires allowlisting
- Request violates organization policy

From [Gemini API troubleshooting](https://ai.google.dev/gemini-api/docs/troubleshooting):
- Free tier not available in region
- Billing not enabled

## Solution

Add specific handling for `ClientError` with full detail extraction:

```python
except Exception as e:
    error_message = str(e)
    status_code = None

    # Enhanced logging for ClientError (Gemini API)
    if hasattr(e, '__class__') and e.__class__.__name__ == 'ClientError':
        # Extract full error details from ClientError
        try:
            details = getattr(e, 'details', None)
            code = getattr(e, 'code', None)
            status = getattr(e, 'status', None)
            message = getattr(e, 'message', None)

            logging_util.error(
                f"🔍 GEMINI_CLIENT_ERROR_DETAILS: "
                f"code={code}, "
                f"status={status}, "
                f"message={message}, "
                f"details={details}"
            )

            # Log full error dict in pretty format for easier debugging
            if details and isinstance(details, dict):
                import json
                logging_util.error(
                    f"🔍 GEMINI_ERROR_FULL_JSON:\n{json.dumps(details, indent=2)}"
                )

            # Check for specific precondition failures
            if details and isinstance(details, dict):
                error_dict = details.get('error', {})
                error_details = error_dict.get('details', [])

                if error_details:
                    logging_util.error(
                        f"🔍 GEMINI_ERROR_NESTED_DETAILS: {error_details}"
                    )

                    # Log any field violations or specific constraints
                    for detail in error_details:
                        if isinstance(detail, dict):
                            detail_type = detail.get('@type', 'unknown')
                            logging_util.error(
                                f"🔍 GEMINI_ERROR_DETAIL_TYPE: {detail_type}, content: {detail}"
                            )
        except Exception as detail_err:
            logging_util.error(f"Failed to extract error details: {detail_err}")

    # Existing error handling continues...
    if hasattr(e, "status_code"):
        status_code = e.status_code
    elif hasattr(e, "response") and hasattr(e.response, "status_code"):
        status_code = e.response.status_code
    # ... rest of existing code
```

## Implementation Location

**File**: `mvp_site/llm_service.py`
**Lines**: 1689-1717 (exception handler in `_call_llm_api()`)
**Change**: Add ClientError-specific logging BEFORE the generic error handling

## Expected Output

After implementation, we'll see logs like:

```
🔍 GEMINI_CLIENT_ERROR_DETAILS: code=400, status=FAILED_PRECONDITION, message=Precondition check failed., details={'error': {'code': 400, 'message': 'Request exceeds model input token limit of 1048576 tokens', 'status': 'FAILED_PRECONDITION', 'details': [...]}}

🔍 GEMINI_ERROR_FULL_JSON:
{
  "error": {
    "code": 400,
    "message": "Request exceeds model input token limit of 1048576 tokens",
    "status": "FAILED_PRECONDITION",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "TOKEN_LIMIT_EXCEEDED",
        "domain": "generativelanguage.googleapis.com"
      }
    ]
  }
}

🔍 GEMINI_ERROR_NESTED_DETAILS: [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'TOKEN_LIMIT_EXCEEDED', ...}]

🔍 GEMINI_ERROR_DETAIL_TYPE: type.googleapis.com/google.rpc.ErrorInfo, content: {'@type': ..., 'reason': 'TOKEN_LIMIT_EXCEEDED', ...}
```

## Benefits

1. **Root Cause Identification**: See exactly which precondition failed
2. **Token Limit Debugging**: Know if request is too large
3. **Policy Violations**: Understand organization policy issues
4. **Better Debugging**: Full error context instead of generic message

## Testing

1. Trigger FAILED_PRECONDITION error (wait for next occurrence)
2. Check logs for new detailed error messages
3. Verify we get specific reason (token limit, location, etc.)
4. Update bead with actual root cause once identified

## Related Issues

- BEAD: gemini-failed-precondition-error.md (investigation)
- PR #3963: Field reordering (unrelated, but good to rule out)
- Community reports: Gemini 3 Preview model instability

## References

- [googleapis/python-genai error.py source](https://github.com/googleapis/python-genai/blob/main/google/genai/errors.py)
- [Vertex AI API errors](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-reference/api-errors)
- [Gemini API troubleshooting](https://ai.google.dev/gemini-api/docs/troubleshooting)

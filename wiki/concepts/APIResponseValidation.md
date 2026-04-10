---
title: "API Response Validation"
type: concept
tags: [api, validation, types, error-handling]
sources: ["type-safety-foundation-tests"]
last_updated: 2026-04-08
---

## Definition
API response validation ensures that responses from external API calls conform to expected structures before processing. Different validation rules apply based on the success state of the response.

## Validation Patterns
- **Success Response**: Requires campaign_id or other success-specific fields
- **Error Response**: Requires error message field
- **Type Checking**: Validates boolean success field and string/structured error fields
- **Rejection Criteria**: None, empty objects, wrong types for success field

## Implementation Pattern
```python
def _validate_api_response(response):
    if not response or not isinstance(response, dict):
        return False
    if "success" not in response:
        return False
    if not isinstance(response["success"], bool):
        return False
    if response["success"]:
        return "campaign_id" in response and response["campaign_id"] is not None
    return "error" in response
```

## Related Concepts
- [[TypeGuards]] — underlying validation mechanism
- [[ErrorHandlingPatterns]] — handling validation failures
- [[TypeSafety]] — the property being enforced

## Sources
- [[Type Safety Foundation Tests]] — test suite for API response validation

---
title: "Type Guards"
type: concept
tags: [typescript, types, runtime-validation, programming]
sources: ["type-safety-foundation-tests"]
last_updated: 2026-04-08
---

## Definition
Type guards are runtime checks that narrow down the type of a variable within a conditional block, enabling TypeScript to make more specific type inferences. They serve as a bridge between compile-time type checking and runtime validation.

## Key Patterns
- **Object Type Checking**: Validating that an object exists and is a dictionary
- **Field Existence**: Checking required fields are present
- **Field Type Validation**: Ensuring field values match expected types
- **Optional Field Handling**: Distinguishing between absent (None) and invalid (wrong type)

## Example Implementation
```python
def _validate_campaign_object(campaign):
    if not campaign or not isinstance(campaign, dict):
        return False
    if not campaign.get("id") or not isinstance(campaign.get("id"), str):
        return False
    if not campaign.get("title") or not isinstance(campaign.get("title"), str):
        return False
    return True
```

## Use Cases
- Campaign object validation before database operations
- API response structure validation
- User input validation in forms
- Firestore document type checking

## Related Concepts
- [[TypeSafety]] — the broader property type guards enforce
- [[APIResponseValidation]] — type guards for API responses
- [[ErrorHandlingPatterns]] — responding to guard failures

## Sources
- [[Type Safety Foundation Tests]] — test suite demonstrating type guard patterns

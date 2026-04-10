---
title: "Backward Compatibility"
type: concept
tags: [api, compatibility, versioning, testing]
sources: ["api-response-format-consistency", "api-backward-compatibility-tests"]
last_updated: 2026-04-08
---

## Definition

Backward compatibility in API design means new versions of the service continue to work with existing client code without requiring changes on the client side.

## Implementation Strategies

### Response Format Preservation
- Maintain direct array responses when legacy code uses `.forEach()`
- Preserve field names and structure in response objects
- Avoid wrapping previously-unwrapped responses

### Testing for Compatibility
- Create integration tests that validate legacy client patterns work
- Test against real response structures, not mocks alone
- Include frontend code patterns (like forEach iteration) in test scenarios

## Common Pitfalls

- Adding object wrappers to previously-array endpoints
- Renaming fields without deprecation notice
- Changing response types (array to object or vice versa)

## Related Concepts
- [[APIResponseFormatConsistency]] — maintaining format standards
- [[APITesting]] — validating API contracts

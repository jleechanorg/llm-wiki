---
title: "API Response Format Consistency"
type: concept
tags: [api, response-format, consistency, testing]
sources: ["api-response-format-consistency", "api-backward-compatibility-tests"]
last_updated: 2026-04-08
---

## Definition

API Response Format Consistency refers to the practice of maintaining uniform response structures across API endpoints to ensure compatibility with various frontend clients and prevent breaking changes.

## Key Patterns

### Array vs Object Wrappers
- Legacy endpoints return arrays directly (e.g., `GET /api/campaigns` returns `[...]`)
- Newer endpoints may wrap in objects (e.g., `{data: [...], success: true}`)
- Frontend code using `forEach` requires direct array access

### Response Structure Standards
- **List endpoints**: Direct array for iteration compatibility
- **Detail endpoints**: Object with named fields (campaign, story, game_state)
- **Creation endpoints**: Object with success boolean and identifier

## Testing Approach

1. Validate each endpoint's response format matches expected structure
2. Test backward compatibility with legacy frontend code
3. Mock Firebase/Auth dependencies to isolate API layer testing

## Related Concepts
- [[BackwardCompatibility]] — maintaining API contract across versions
- [[APIResponseFormat]] — JSON structure conventions

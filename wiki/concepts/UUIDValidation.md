---
title: "UUID Validation"
type: concept
tags: [validation, uuid, security, input-validation]
sources: [input-validation-utilities]
last_updated: 2026-04-08
---

## Definition
UUID validation is a pattern for validating identifiers in the UUID format (e.g., `550e8400-e29b-41d4-a716-446655440000`) or as safe alphanumeric strings with dashes/underscores.

## Usage in This Project
Used to validate `campaign_id` and `user_id` parameters to prevent injection or abuse through malformed identifiers.

## Key Details
- UUID pattern: `^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$`
- Alphanumeric pattern: `^[a-zA-Z0-9_-]+$`
- Max length: 128 characters to prevent abuse

## Related
- [[InputValidationUtilities]]
- [[RequestSizeValidation]]

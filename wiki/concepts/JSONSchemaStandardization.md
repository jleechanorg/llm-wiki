---
title: "JSON Schema Standardization"
type: concept
tags: [json, api, schema, standardization]
sources: [unified-api-implementation]
last_updated: 2026-04-08
---

## Definition
Practice of defining consistent JSON input/output formats across all API endpoints, ensuring uniform error handling and response structures.

## WorldArchitect.AI Standard Format

**Input:** `{user_id, campaign_id, ...function_params}`

**Success Response:** `{success: true, ...function_data}`


**Error Response:** `{success: false, error: string, status_code: number}`

## Related Concepts
- [[UnifiedAPIPattern]]
- [[ErrorHandling]]

---
title: "Dependency Injection"
type: concept
tags: [design-pattern, testing]
sources: ["fallback-behavior-review-mvp-site"]
last_updated: 2026-04-08
---

Software design pattern where dependencies are provided to components rather than components creating them. The mvp_site review addressed strictness of injection.

## MCP Memory Client Implementation
- `set_functions()` helper requires all three MCP functions together
- Partial injection rejected to avoid inconsistent states
- Missing handlers cause immediate failure

## Rationale
Strict dependency injection surfaces configuration errors immediately rather than failing later with confusing errors.

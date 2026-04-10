---
title: "Code Centralization"
type: concept
tags: [refactoring, software-engineering, patterns]
sources: [code-centralization-testing-utils-deduplication]
last_updated: 2026-04-08
---

Software engineering pattern where duplicate or similar code across multiple modules is consolidated into a single canonical location. In this case, testing utilities scattered across testing_mcp and testing_ui are being centralized into testing_utils.

## Benefits
- Single source of truth for shared functionality
- Easier maintenance — fixes apply everywhere
- Reduced code duplication
- Consistent behavior across consumer modules

## Implementation
- Remove duplicate function definitions from consumer modules
- Import canonical implementations from the centralized module
- Use delegation (re-export) patterns where appropriate

## Related Concepts
- [[FunctionDelegation]] — pattern for forwarding calls
- [[DRYPrinciple]] — Don't Repeat Yourself
- [[ModuleRefactoring]] — structural code changes

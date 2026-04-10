---
title: "Debouncing"
type: concept
tags: [performance, optimization, timing]
sources: [enhanced-search-filter-milestone-4]
last_updated: 2026-04-08
---

## Description
Performance optimization technique that limits the rate at which a function fires by waiting until a specified delay has elapsed since the last invocation. Used in EnhancedSearch with a 300ms wait time.

## Use Case
Search input where each keystroke would otherwise trigger an expensive operation (API call, DOM update). Debouncing ensures the operation only fires after the user stops typing.

## Related Concepts
- [[RealTimeSearch]] — primary use case
- [[Throttling]] — similar but allows periodic firing

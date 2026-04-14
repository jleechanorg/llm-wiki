---
title: "TanStack Query State Management"
type: concept
tags: [canonical, typescript, tanstack, state-management, caching]
sources: [canonical-code-repos/tanstack-query]
last_updated: 2026-04-14
---

## Summary

TanStack Query (formerly React Query) solves a specific problem: server state is different from client state and needs different patterns. It manages async lifecycle (loading, error, data) separately from UI state, with automatic background refetching, deduplication, and cache invalidation. The architecture: a `QueryClient` owns a `QueryCache` that holds `QueryObserver` instances per unique key.

## Key Patterns

### Separation: Query Cache + Query Observer
```typescript
// QueryCache: stores all query results globally
export { QueryCache } from './queryCache'
export { QueryObserver } from './queryObserver'
export { MutationCache } from './mutationCache'
export { MutationObserver } from './mutationObserver'
```

Cache and observer are separate. Cache holds raw data; observers hold subscription state. Multiple components can observe the same query key.

### Focus/Online Managers
```typescript
export { focusManager } from './focusManager'
export { onlineManager } from './onlineManager'
export { defaultScheduler, notifyManager } from './notifyManager'
```

Separation of concerns: `focusManager` tracks window focus for background refetch, `onlineManager` tracks network, `notifyManager` batches subscriber notifications.

### Deduplication by Default
```typescript
export { hashKey } from './utils'  // consistent hash for query keys
export { keepPreviousData } from './utils'  // don't flash loading on refetch
```

Query keys are deterministically hashed. Two components requesting the same key share one fetch. `keepPreviousData` prevents the "flash of loading state" on refetch.

### Dehydration / Hydration
```typescript
export { dehydrate, hydrate } from './hydration'
export type { DehydratedState, DehydrateOptions, HydrateOptions } from './hydration'
```

Server-side rendering support: queries are dehydrated (serialized) on server and rehydrated (restored) on client. Cache survives SSR.

### Cancellation + Retry
```typescript
export { CancelledError, isCancelledError } from './retryer'
```

Built-in retry with exponential backoff. Cancellations are errors with specific type — can be caught and handled differently.

## What This Means for Code Generation

Generated async data-fetching code should:
1. Use a query key system — consistent, hashable, hierarchical keys
2. Separate lifecycle states: `isLoading`, `isError`, `isSuccess`, `isFetching`
3. Never refetch on every render — deduplicate and cache aggressively
4. Include background refetch on window focus / online status
5. Provide `keepPreviousData` semantics — don't flash loading on updates
6. Support SSR dehydration if the codebase uses server rendering

---
title: "Runtime Deduplication"
type: concept
tags: [symphony, deduplication, runtime]
sources: [symphony-runtime-dedupe-contract]
last_updated: 2026-04-07
---

## Definition
The process of ensuring Symphony daemon operations avoid duplicating work by maintaining clear boundaries between local curation layers and runtime primitives. Local extensions (plugins, benchmarks) remain in the repository while runtime logic lives in Symphony.


## Key Principles
- **Local retention**: Repository-specific curation stays local (`scripts/`, `openclaw-config/`)
- **Runtime primitives**: Generic workflow logic lives in Symphony runtime
- **Clear boundaries**: No policy expansion at daemon bootstrap time

## Related Concepts
- [[DaemonBootstrap]] — where deduplication contract applies
- [[PluginPayload]] — shaped locally, dispatched via runtime

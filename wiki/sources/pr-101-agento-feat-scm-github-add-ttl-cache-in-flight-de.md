---
title: "PR #101: [agento] feat(scm-github): add TTL cache + in-flight dedupe for gh API calls"
type: source
tags: []
date: 2026-03-22
source_file: raw/prs-worldai_claw/pr-101.md
sources: []
last_updated: 2026-03-22
---

## Summary
- Adds `gh-cache.ts`: a shared 15-second TTL cache with in-flight request deduplication for all `gh` CLI read calls in the scm-github plugin
- Caches `gh api`, `gh pr view`, and `gh pr checks` by full arg array + cwd key
- Concurrent sessions targeting the same PR now share one network round-trip per poll cycle
- Exports `getGhCache()` and `GhCache.metrics` for observability
- Zero impact on write operations (merge, close, create — never cached)

## Metadata
- **PR**: #101
- **Merged**: 2026-03-22
- **Author**: jleechan2015
- **Stats**: +469/-20 in 6 files
- **Labels**: none

## Connections

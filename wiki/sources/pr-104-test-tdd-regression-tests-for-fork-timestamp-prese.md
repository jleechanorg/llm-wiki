---
title: "PR #104: test: TDD regression tests for fork() timestamp preservation (WC-fr8)"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-104.md
sources: []
last_updated: 2026-03-26
---

## Summary
`fork()` in `packages/backend/src/storage/entity_chain.ts` previously used `append()` which calls `Date.now()` for each block, destroying original timestamps. The `appendWithTimestamp()` private method was added to preserve original block timestamps when forking entity chains. However, no regression tests existed to guard this behavior.

## Metadata
- **PR**: #104
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +186/-0 in 1 files
- **Labels**: none

## Connections

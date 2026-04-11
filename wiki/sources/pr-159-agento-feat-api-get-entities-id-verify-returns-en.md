---
title: "PR #159: [agento] feat(api): GET /entities/:id/verify returns {entityId, chainLength, lastHash, verified}"
type: source
tags: []
date: 2026-03-31
source_file: raw/prs-worldai_claw/pr-159.md
sources: []
last_updated: 2026-03-31
---

## Summary
- Updates GET /entities/:id/verify route to use getEntityChain() factory and return the required shape {entityId, chainLength, lastHash, verified: boolean}
- Exports hashBlock() from entity_chain.ts for computing the last block hash
- Updates existing integration test to assert the new response shape

## Metadata
- **PR**: #159
- **Merged**: 2026-03-31
- **Author**: jleechan2015
- **Stats**: +120/-38 in 3 files
- **Labels**: none

## Connections

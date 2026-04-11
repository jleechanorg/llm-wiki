---
title: "PR #329: chore: hash shared libs builds and drop dist artifacts"
type: source
tags: [codex]
date: 2025-10-14
source_file: raw/prs-/pr-329.md
sources: []
last_updated: 2025-10-14
---

## Summary
- add content-hash helpers for shared libs (compute script, staging verifier, run-build-if-ready) and switch prepare logic to hash comparison + persisted .src-hash files
- copy shared build scripts into Docker images/deploy contexts so file: dependencies install correctly with prebuilt dist assets
- update backend coverage workflow to rebuild shared libs with fresh npm cache, eliminating stale dist exports behind the Node 22 backend validation failure
- drop previously committed dist artifacts a

## Metadata
- **PR**: #329
- **Merged**: 2025-10-14
- **Author**: jleechan2015
- **Stats**: +421/-96 in 19 files
- **Labels**: codex

## Connections

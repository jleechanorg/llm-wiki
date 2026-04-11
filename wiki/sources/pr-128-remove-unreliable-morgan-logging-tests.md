---
title: "PR #128: Remove unreliable Morgan logging tests"
type: source
tags: [codex]
date: 2025-11-05
source_file: raw/prs-/pr-128.md
sources: []
last_updated: 2025-11-05
---

## Summary
- delete the permanently skipped Morgan logging Vitest suite that depended on real HTTP traffic
- document in `server.cjs` that Morgan logging is validated via manual smoke tests due to MSW intercepts in unit tests

## Metadata
- **PR**: #128
- **Merged**: 2025-11-05
- **Author**: jleechan2015
- **Stats**: +34/-315 in 3 files
- **Labels**: codex

## Connections

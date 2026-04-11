---
title: "PR #326: [agento] test(lifecycle): add bd-n039 send-to-agent SHA dedup unit tests"
type: source
tags: []
date: 2026-03-31
source_file: raw/prs-worldai_claw/pr-326.md
sources: []
last_updated: 2026-03-31
---

## Summary
bd-n039 introduced SHA-based deduplication for send-to-agent reactions in lifecycle-manager.ts, preventing redundant message sends when the PR head SHA is unchanged. The implementation (dedup-head-sha-store.ts) was merged but lacked a dedicated unit test file.

## Metadata
- **PR**: #326
- **Merged**: 2026-03-31
- **Author**: jleechan2015
- **Stats**: +298/-0 in 1 files
- **Labels**: none

## Connections

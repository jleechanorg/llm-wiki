---
title: "PR #315: [agento] fix(security): restore fork PR runner protection and ARM64 gitleaks checksum"
type: source
tags: []
date: 2026-03-31
source_file: raw/prs-worldai_claw/pr-315.md
sources: []
last_updated: 2026-03-31
---

## Summary
PR #302 (message-content hash dedup) was branched before PR #273 (self-hosted runners with fork protection) merged. When #302 was squash-merged, it silently reverted all security protections from #273 across 6 workflow files.

## Metadata
- **PR**: #315
- **Merged**: 2026-03-31
- **Author**: jleechan2015
- **Stats**: +308/-320 in 13 files
- **Labels**: none

## Connections

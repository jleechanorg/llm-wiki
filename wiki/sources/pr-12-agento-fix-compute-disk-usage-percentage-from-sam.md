---
title: "PR #12: [agento] fix: compute disk usage percentage from same basis as used_gb"
type: source
tags: []
date: 2026-04-02
source_file: raw/prs-/pr-12.md
sources: []
last_updated: 2026-04-02
---

## Summary
The disk usage alert script was reporting inconsistent metrics: `Used: 796G of 926G (12%)`. The percentage shown (12%) did not match the actual used/total ratio (796/926 ≈ 86%).

Root cause: script computes `used_gb` correctly as `total - available` (APFS-aware) but printed percentage from raw `df $5` field, which under-reports used space on APFS because it only counts non-purgeable blocks.

## Metadata
- **PR**: #12
- **Merged**: 2026-04-02
- **Author**: jleechan2015
- **Stats**: +3/-1 in 1 files
- **Labels**: none

## Connections

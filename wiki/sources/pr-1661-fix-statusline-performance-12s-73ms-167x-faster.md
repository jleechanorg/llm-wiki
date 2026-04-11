---
title: "PR #1661: Fix statusLine performance: 12s → 73ms (167x faster)"
type: source
tags: []
date: 2025-09-21
source_file: raw/prs-worldarchitect-ai/pr-1661.md
sources: []
last_updated: 2025-09-21
---

## Summary
- Optimized git-header.sh for Claude Code statusLine from 12+ seconds to 73ms
- Removed slow GitHub CLI API calls that caused timeouts
- Added uncommitted changes detection for better development workflow awareness
- Preserved essential information while eliminating performance bottlenecks

## Metadata
- **PR**: #1661
- **Merged**: 2025-09-21
- **Author**: jleechan2015
- **Stats**: +310/-265 in 2 files
- **Labels**: none

## Connections

---
title: "PR #1923: Fix savetmp artifact collision handling"
type: source
tags: [codex]
date: 2025-10-30
source_file: raw/prs-worldarchitect-ai/pr-1923.md
sources: []
last_updated: 2025-10-30
---

## Summary
- track reserved targets so /savetmp never reuses artifact filenames within a run
- apply the same collision-free logic when copying directories and sanitize work names against all separators
- update typing imports to include Set for the reserved target tracking

## Metadata
- **PR**: #1923
- **Merged**: 2025-10-30
- **Author**: jleechan2015
- **Stats**: +425/-0 in 3 files
- **Labels**: codex

## Connections

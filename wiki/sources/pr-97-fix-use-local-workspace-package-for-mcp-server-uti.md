---
title: "PR #97: fix: Use local workspace package for mcp-server-utils"
type: source
tags: []
date: 2025-09-30
source_file: raw/prs-/pr-97.md
sources: []
last_updated: 2025-09-30
---

## Summary
- Fixed deployment build failure by switching `@ai-universe/mcp-server-utils` from npm registry reference to local workspace package
- Excluded test files from TypeScript build to prevent compilation errors
- Ensures consistency with other `@ai-universe/*` shared-libs packages

## Metadata
- **PR**: #97
- **Merged**: 2025-09-30
- **Author**: jleechan2015
- **Stats**: +68/-17 in 8 files
- **Labels**: none

## Connections

---
title: "PR #5872: fix: add missing check_github_requirements to scripts/mcp_common.sh"
type: source
tags: []
date: 2026-03-08
source_file: raw/prs-worldarchitect-ai/pr-5872.md
sources: []
last_updated: 2026-03-08
---

## Summary
- `check_github_requirements` was called on line 1249 of `scripts/mcp_common.sh` but never defined, causing the MCP installer to crash with exit code 127 on every run
- Synced the function definition from `.claude/scripts/mcp_common.sh` (the canonical version)

## Metadata
- **PR**: #5872
- **Merged**: 2026-03-08
- **Author**: jleechan2015
- **Stats**: +26/-0 in 1 files
- **Labels**: none

## Connections

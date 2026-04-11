---
title: "PR #46: Use CLAUDE_API_KEY consistently"
type: source
tags: [codex]
date: 2025-09-25
source_file: raw/prs-/pr-46.md
sources: []
last_updated: 2025-09-25
---

## Summary
- replace all usage of the deprecated `ANTHROPIC_API_KEY` environment variable with `CLAUDE_API_KEY`
- update deployment scripts, docs, and test utilities to reflect the new variable name
- simplify secret manager mapping now that only `CLAUDE_API_KEY` is supported

## Metadata
- **PR**: #46
- **Merged**: 2025-09-25
- **Author**: jleechan2015
- **Stats**: +10/-14 in 10 files
- **Labels**: codex

## Connections

---
title: "PR #203: fix: orchestration CLI integration test model placeholder and tool validation"
type: source
tags: []
date: 2026-02-02
source_file: raw/prs-/pr-203.md
sources: []
last_updated: 2026-02-02
---

## Summary
- Add `{model}` placeholder to `command_template.format()` with default "sonnet" to fix KeyError when orchestration library templates include `{model}`
- Update MCP tool validation to accept either core tools OR extended tools as both indicate successful MCP connectivity

## Metadata
- **PR**: #203
- **Merged**: 2026-02-02
- **Author**: jleechan2015
- **Stats**: +34/-7 in 4 files
- **Labels**: none

## Connections

---
title: "PR #377: chore: remove multi-model synthesis tool + fix auto-resolve CI triggers"
type: source
tags: [codex]
date: 2025-10-17
source_file: raw/prs-/pr-377.md
sources: []
last_updated: 2025-10-17
---

## Summary
### Primary Changes
- Remove the standalone multi-model opinion synthesis tool from the backend registry and agent wiring
- Delete the dedicated unit and integration tests that targeted the removed tool implementation
- Update smoke test documentation to reflect the reduced MCP tool surface
- Remove the lingering ToolRegistry reset assignment that referenced the deleted multi-model tool

### Auto-Resolve Workflow Improvements (Added in this PR)

**Problem Fixed:** Auto-resolve commits using `GIT

## Metadata
- **PR**: #377
- **Merged**: 2025-10-17
- **Author**: jleechan2015
- **Stats**: +122/-28 in 21 files
- **Labels**: codex

## Connections

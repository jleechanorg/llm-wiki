---
title: "PR #17: [agento] feat: open eventType to any string (#jleechan-oe36)"
type: source
tags: []
date: 2026-03-27
source_file: raw/prs-/pr-17.md
sources: []
last_updated: 2026-03-27
---

## Summary
`PostEventTypeSchema` in `src/shared/types.ts` was a closed `z.enum()` listing only AO/PR-specific values (`pr_created`, `pr_merged`, `novel_branch_entry`, etc.). Any caller wanting to use a custom event type (e.g., `issue_created`, `deploy_started`, `custom_workflow_event`) would get a Zod validation error.

## Metadata
- **PR**: #17
- **Merged**: 2026-03-27
- **Author**: jleechan2015
- **Stats**: +7/-3 in 1 files
- **Labels**: none

## Connections
